from abc import ABCMeta
from abc import abstractmethod
from collections import Counter, defaultdict
import re

try:
    xrange
    range = xrange
    iteritems = lambda d: d.iteritems()
except NameError:
    iteritems = lambda d: d.items()


class RequiresTraining(Exception):
    """ Raised when training is required. """
    pass


class BaseObject(object):
    def __init__(self, *args, **kwargs):
        super(BaseObject, self).__init__()


class AbstractTokenizer(BaseObject):

    __metaclass__ = ABCMeta

    def __init__(self, min_n_gram_size=1, **extras):
        self.min_n_gram_size = min_n_gram_size
        super(AbstractTokenizer, self).__init__(**extras)

    @abstractmethod
    def _store_token_to_full_string(self, token_to_full_string_dict):
        pass

    @abstractmethod
    def _store_n_gram_to_tokens(self, n_gram_to_tokens_dict):
        pass

    @abstractmethod
    def _clear_tokenizer_storage(self):
        pass

    @abstractmethod
    def get_full_strings_for_token(self, token, default_empty=None):
        pass

    @abstractmethod
    def get_tokens_for_n_gram(self, n_gram, default_empty=None):
        pass

    def bust_cache(self):
        """ Clears all cached values. """
        self._clear_tokenizer_storage()

    def _to_alpha_numeric(self, input_string):
        return ''.join(ch.lower() for ch in input_string if ch.isalnum() or ch == ' ')

    def train_from_strings(self, input_string_list):
        """ Trains the tokenizer such that input tokens from a user can
        be mapped to the strings input here. """
        token_to_full_string = defaultdict(set)
        n_gram_to_tokens = defaultdict(set)

        for input_string in input_string_list:
            alpha_numeric_input_string = self._to_alpha_numeric(input_string)
            tokens = alpha_numeric_input_string.split()
            for token in tokens:
                token_to_full_string[token].add(input_string)
                if len(token) < self.min_n_gram_size:
                    n_gram_to_tokens[token].add(token)
                for string_size in range(self.min_n_gram_size, len(token) + 1):
                    n_gram = token[:string_size]
                    n_gram_to_tokens[n_gram].add(token)

        self._store_token_to_full_string(dict(token_to_full_string))
        self._store_n_gram_to_tokens(dict(n_gram_to_tokens))


class AbstractSpellChecker(AbstractTokenizer):

    __metaclass__ = ABCMeta

    def __init__(self, typo_deviations=2, max_word_length=10, **extras):
        self.typo_deviations = typo_deviations
        self.max_word_length = max_word_length
        super(AbstractSpellChecker, self).__init__(**extras)

    def _to_alpha_words_list(self, text):
        return re.findall('[a-z]+', text.lower())

    @abstractmethod
    def get_count_for_token(self, token, default_empty=0):
        pass

    @abstractmethod
    def get_counts_for_tokens(self, token_list, default_empty=0):
        pass

    @abstractmethod
    def _store_token_to_count(self):
        pass

    @abstractmethod
    def _clear_spellcheck_storage(self):
        pass

    def bust_cache(self):
        """ Clears the cache so that model can be re-trained. """
        super(AbstractSpellChecker, self).bust_cache()
        self._clear_spellcheck_storage()

    def _possible_typos(self, word):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts = [a + c + b for a, b in splits for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def _extended_typos(self, word):
        if len(word) >= self.max_word_length:
            return set()
        deviations = self._possible_typos(word)
        all_deviations = set() | deviations
        for _ in range(self.typo_deviations - 1):
            deviations = \
                {item for deviation in deviations for item in self._possible_typos(deviation)}
            all_deviations |= deviations
        deviation_to_count = self.get_counts_for_tokens(all_deviations)
        return {deviation for deviation in all_deviations if deviation_to_count[deviation]}

    def _words_that_exist(self, words):
        return set(w for w in words if self.get_count_for_token(w))

    def train_from_strings(self, input_string_list):
        """ Mutates the class such that input text from the user can be
        auto corrected to the input provided here. """
        super(AbstractSpellChecker, self).train_from_strings(input_string_list)

        token_to_count = Counter()
        for input_string in input_string_list:
            alpha_words = self._to_alpha_words_list(input_string)
            for token in alpha_words:
                token_to_count[token] += 1
        self._store_token_to_count(dict(token_to_count))

    def correct_token(self, token):
        """ Given an input token, returns a valid token present in the trained model. """
        token = token.lower()
        if self.get_tokens_for_n_gram(token) is not None:
            return token
        candidates = (self._words_that_exist([token]) or
                      self._words_that_exist(self._possible_typos(token)) or
                      self._extended_typos(token) or
                      [token])
        return max(candidates, key=self.get_count_for_token)

    def correct_phrase(self, text):
        """ Given an input blob of text, returns a list of valid tokens that can be used
        for autocomplete. """
        tokens = text.split()
        return [self.correct_token(token) for token in tokens]


class AbstractAutoCompleter(AbstractSpellChecker):

    __metaclass__ = ABCMeta

    def __init__(self, min_results=5, max_results=10, score_threshold=0.2, **extras):
        self.min_results = min_results
        self.max_results = max_results
        self.score_threshold = score_threshold
        super(AbstractAutoCompleter, self).__init__(**extras)

    def _get_real_tokens_from_possible_n_grams(self, tokens):
        real_tokens = set()
        for token in tokens:
            token_set = self.get_tokens_for_n_gram(token, set())
            real_tokens |= token_set
        return real_tokens

    def _get_scored_strings_uncollapsed(self, real_tokens):
        all_full_strings = set.union(*[self.get_full_strings_for_token(token, set()) for token in real_tokens] + [set()])

        def _get_score(full_string):
            exact_tokens_matched = len(real_tokens) - len(set(real_tokens) - set(full_string.split(" ")))
            percent_match_tokens = float(exact_tokens_matched) / len(real_tokens)

            all_token_characters = list("".join(real_tokens))
            all_string_characters = list(full_string.replace(" ", ""))
            filtered_string = all_string_characters
            for match_character in all_token_characters:
                for outer_index, cursor_character in enumerate(filtered_string):
                    if cursor_character == match_character:
                        filtered_string = "".join([char for index, char in enumerate(filtered_string) if index != outer_index])
                        break
            characters_consumed = len(all_string_characters) - len(filtered_string)
            percent_match_raw = float(characters_consumed) / len(all_string_characters)
            return 0.66 * percent_match_tokens + 0.333 * percent_match_raw

        full_string__scores = [(s, _get_score(s)) for s in all_full_strings]
        return sorted(full_string__scores, key=lambda t: t[1], reverse=True)

    def _combined_scores(self, full_string__scores, num_tokens):
        collapsed_string_to_score = defaultdict(int)
        collapsed_string_to_occurence = defaultdict(int)
        for full_string, score in full_string__scores:
            collapsed_string_to_score[full_string] += score
            collapsed_string_to_occurence[full_string] += 1
        for full_string in collapsed_string_to_score.keys():
            percent_match = collapsed_string_to_occurence[full_string] / float(num_tokens)
            collapsed_string_to_score[full_string] *= percent_match
        return collapsed_string_to_score

    def _filtered_results(self, full_string__scores):
        max_possibles = full_string__scores[:self.max_results]
        if full_string__scores and full_string__scores[0][1] == 1.0:
            exact_match_str = full_string__scores[0][0]
            min_len = len(exact_match_str)
            full_string__scores = \
                [tuple_obj for tuple_obj in full_string__scores if len(tuple_obj[0]) >= min_len]

        possibles_within_thresh = \
            [tuple_obj for tuple_obj in full_string__scores if tuple_obj[1] >= self.score_threshold]
        if len(possibles_within_thresh) > self.min_results:
            min_possibles = possibles_within_thresh[:self.max_results]
        else:
            min_possibles = max_possibles[:self.min_results]
        return [tuple_obj[0] for tuple_obj in min_possibles]

    def _cleaned_tokens(self, token_list):
        cleaned_tokens = []
        for token in token_list:
            try:
                unicode(token)
            except UnicodeDecodeError:
                continue
            cleaned_tokens.append(token)
        return cleaned_tokens

    def guess_full_strings(self, token_list):
        """ Given an input list of tokens, returns an ordered list of phrases
        that most likely aligns with the input. """
        real_tokens = self._get_real_tokens_from_possible_n_grams(token_list)
        real_tokens = self._cleaned_tokens(real_tokens)
        full_string__scores = self._get_scored_strings_uncollapsed(real_tokens)
        collapsed_string_to_score = self._combined_scores(full_string__scores, len(token_list))
        full_string__scores = sorted(iteritems(collapsed_string_to_score),
                                     key=lambda t: t[1], reverse=True)
        return self._filtered_results(full_string__scores)


class DictStorageTokenizer(AbstractTokenizer):

    def __init__(self, dict_obj, **extras):
        self._cls_cache = dict_obj
        super(DictStorageTokenizer, self).__init__(**extras)

    def get_full_strings_for_token(self, token, default_empty=None):
        attr_key = "token_to_full_string"
        try:
            return self._cls_cache[attr_key].get(token, default_empty)
        except KeyError:
            raise RequiresTraining("Must call train_from_strings() before using this property")

    def _store_token_to_full_string(self, token_to_full_string_dict):
        attr_key = 'token_to_full_string'
        if attr_key not in self._cls_cache:
            self._cls_cache[attr_key] = token_to_full_string_dict
        else:
            for token, full_string_set in iteritems(token_to_full_string_dict):
                try:
                    self._cls_cache[attr_key][token] |= full_string_set
                except KeyError:
                    self._cls_cache[attr_key][token] = full_string_set

    def get_tokens_for_n_gram(self, n_gram, default_empty=None):
        attr_key = "n_gram_to_tokens"
        try:
            return self._cls_cache[attr_key].get(n_gram, default_empty)
        except KeyError:
            raise RequiresTraining("Must call train_from_strings() before using this property")

    def _store_n_gram_to_tokens(self, n_gram_to_tokens_dict):
        attr_key = 'n_gram_to_tokens'
        if attr_key not in self._cls_cache:
            self._cls_cache[attr_key] = n_gram_to_tokens_dict
        else:
            for n_gram, token_set in iteritems(n_gram_to_tokens_dict):
                try:
                    self._cls_cache[attr_key][n_gram] |= token_set
                except KeyError:
                    self._cls_cache[attr_key][n_gram] = token_set

    def _clear_tokenizer_storage(self):
        self._cls_cache.clear()


class DictStorageSpellChecker(DictStorageTokenizer, AbstractSpellChecker):

    def get_counts_for_tokens(self, token_list, default_empty=0):
        attr_key = "token_to_count"
        if not self._cls_cache[attr_key]:
            raise RequiresTraining("Must call train_from_strings() before using this property")
        return {token: self._cls_cache[attr_key].get(token, default_empty) for token in token_list}

    def get_count_for_token(self, token, default_empty=0):
        attr_key = "token_to_count"
        try:
            return self._cls_cache[attr_key].get(token, default_empty)
        except KeyError:
            raise RequiresTraining("Must call train_from_strings() before using this property")

    def _store_token_to_count(self, token_to_count_dict):
        attr_key = 'token_to_count'
        if attr_key not in self._cls_cache:
            self._cls_cache[attr_key] = token_to_count_dict
        else:
            for token, count in iteritems(token_to_count_dict):
                try:
                    self._cls_cache[attr_key][token] += count
                except KeyError:
                    self._cls_cache[attr_key][token] = count

    def _clear_spellcheck_storage(self):
        try:
            for key in self._cls_cache["token_to_count"].keys():
                del self._cls_cache["token_to_count"][key]
        except KeyError:
            pass


class DictStorageAutoCompleter(DictStorageSpellChecker, AbstractAutoCompleter):
    pass


class RedisStorageTokenizer(AbstractTokenizer):

    def __init__(self, redis_client, use_pipeline=True, **extras):
        super(RedisStorageTokenizer, self).__init__(**extras)
        self.redis_client = redis_client
        self.use_pipeline = use_pipeline

    def get_client(self):
        if self.use_pipeline:
            return self.redis_client.pipeline()
        return self.redis_client

    def get_full_strings_for_token(self, token, default_empty=None):
        try:
            token = token.encode("utf-8")
        except AttributeError:
            pass
        key_count = self.redis_client.scard("token_to_full_string_keys")
        if not key_count:
            raise RequiresTraining("Must call train_from_strings() before using this property")
        full_strings = self.redis_client.smembers(b"token:" + token) or default_empty
        return {s.decode("utf-8") for s in full_strings}

    def _store_token_to_full_string(self, token_to_full_string_dict):
        client = self.get_client()
        for key, full_strings_set in iteritems(token_to_full_string_dict):
            for full_string in full_strings_set:
                client.sadd("token:" + key, full_string)
            client.sadd("token_to_full_string_keys", key)
        if self.use_pipeline:
            client.execute()

    def get_tokens_for_n_gram(self, n_gram, default_empty=None):
        key_count = self.redis_client.scard("n_gram_to_token_key")
        if not key_count:
            raise RequiresTraining("Must call train_from_strings() before using this property")
        return self.redis_client.smembers("n_gram:" + n_gram) or default_empty

    def _store_n_gram_to_tokens(self, n_gram_to_tokens_dict):
        client = self.get_client()
        for n_gram, token_set in iteritems(n_gram_to_tokens_dict):
            for token in token_set:
                client.sadd("n_gram:" + n_gram, token)
            client.sadd("n_gram_to_token_key", n_gram)
        if self.use_pipeline:
            client.execute()

    def _clear_tokenizer_storage(self):
        self._clear_token_to_full_strings()
        self._clear_n_gram_to_tokens()

    def _clear_token_to_full_strings(self):
        token_keys = self.redis_client.smembers("token_to_full_string_keys")
        for key in token_keys:
            try:
                self.redis_client.expire(b"token:" + key, 0)
            except UnicodeDecodeError:
                continue
        self.redis_client.expire("token_to_full_string_keys", 0)

    def _clear_n_gram_to_tokens(self):
        n_gram_keys = self.redis_client.smembers("n_gram_to_token_key")
        for key in n_gram_keys:
            try:
                self.redis_client.expire(b"n_gram:" + key, 0)
            except UnicodeDecodeError:
                continue
        self.redis_client.expire("n_gram_to_token_key", 0)


class RedisStorageSpellChecker(RedisStorageTokenizer, AbstractSpellChecker):

    def get_counts_for_tokens(self, token_list, default_empty=0):
        try:
            int(default_empty)
        except TypeError:
            raise TypeError("default_empty must be an int")

        key_count = self.redis_client.scard("token_to_count_key")
        if not key_count:
            raise RequiresTraining("Must call train_from_strings() before using this property")
        listified_tokens = [token for token in token_list]
        keys = ["count:%s" % token for token in listified_tokens]
        values = self.redis_client.mget(keys)
        token_to_count = {}
        for index, token in enumerate(listified_tokens):

            if index >= len(values):
                # edge case for certain redis wrappers apparently
                redis_value = 0
            else:
                redis_value = int(values[index] or 0)
            token_to_count[token] = redis_value
        return token_to_count

    def get_count_for_token(self, token, default_empty=0):
        try:
            int(default_empty)
        except TypeError:
            raise TypeError("default_empty must be an int")

        key_count = self.redis_client.scard("token_to_count_key")
        if not key_count:
            raise RequiresTraining("Must call train_from_strings() before using this property")
        count = self.redis_client.get("count:" + token) or default_empty
        return int(count)

    def _store_token_to_count(self, token_to_count_dict):
        client = self.get_client()
        for token, count in iteritems(token_to_count_dict):
            count_key = "count:" + token
            client.incr(count_key, count)
            client.sadd("token_to_count_key", token)
        if self.use_pipeline:
            client.execute()

    def _clear_spellcheck_storage(self):
        tokens = self.redis_client.smembers("token_to_count_key")
        for token in tokens:
            self.redis_client.expire(b"count:" + token, 0)
        self.redis_client.expire("token_to_count_key", 0)


class RedisStorageAutoCompleter(RedisStorageSpellChecker, AbstractAutoCompleter):
    pass
