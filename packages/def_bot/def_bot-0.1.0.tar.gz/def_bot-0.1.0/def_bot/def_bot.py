from __future__ import unicode_literals
from drae import drae
from bender import Bot
from bender import final_step
from bender import next_step


class Def(Bot):
    commands = {'/def': 'search_word'}

    def __init__(self, dunno_sticker, go_away_sticker, *args, **kwargs):
        self.dunno_sticker = dunno_sticker
        self.go_away_sticker = go_away_sticker
        super(Def, self).__init__(*args, **kwargs)

    @next_step('define_word')
    def search_word(self, *args, **kwargs):
        word = kwargs.get('rest')
        wx = drae.search(word)

        if wx:
            if isinstance(wx, list):
                # this is ugly
                user_words_key = self.redis_prefix + str(self._message['chat']['id'])
                for w in wx:
                    # save this chat's word choice list
                    self.redis.sadd(user_words_key, w)

                    # save word info (global)
                    self.redis.sadd(self.redis_prefix + 'words', w.word)
                    word_key = self.redis_prefix + 'words:' + w.word
                    self.redis.hset(word_key, 'id', w.id)

                # return True => next step
                return self.reply({'text': 'Which one?',
                                   'reply_markup': {'keyboard': [[w.word for w in wx]],
                                                    'one_time_keyboard': True,
                                                    'selective': True}})
            else:
                # save word info (global)
                word_key = self.redis_prefix + 'words:' + wx.word
                self.redis.sadd(self.redis_prefix + 'words', wx.word)
                self.redis.hset(word_key, 'id', wx.id)
                self.redis.hincrby(word_key, 'hits', 1)
                self.reply({'text': wx.text})
        else:
            return self.reply({'sticker': self.dunno_sticker})

    @final_step
    def define_word(self, *args, **kwargs):
        word = self._message.get('text', '')
        user_words_key = self.redis_prefix + str(self._message['chat']['id'])
        if self.redis.sismember(user_words_key, word):
            word_key = self.redis_prefix + 'words:' + word
            word_id = self.redis.hget(word_key, 'id')

            w = drae.Word(word, word_id)
            meaning = w.text
            self.reply({'text': meaning,
                        'reply_markup': {'hide_keyboard': True}})

            self.redis.delete(user_words_key)
            self.redis.hincrby(word_key, 'hits', 1)
            return True
        else:
            return self.reply({'sticker': self.go_away_sticker,
                               'reply_markup': {'hide_keyboard': True}})
