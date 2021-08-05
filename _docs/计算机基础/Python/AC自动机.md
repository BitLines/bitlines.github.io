
安装 pyahocorasick
> pip install pyahocorasick


```Python
import ahocorasick

class KeywordExtractor(object):
    def __init__(self, user_dict):
        '''
        Params:
            user_dict: Dict，用户词典
        '''
        self._actree = ahocorasick.Automaton()
        for key, value in user_dict.items():
            self._actree.add_word(key, (key, value))
        self._actree.make_automaton()

    def extract(self, text):
        '''
        提取 text 中命中的字符串。
        Params:
            text: str, 输入字符串
        Return:
            ((key, value), start, end)
            key: str, 提出的 dict 中的 key
            value: Any, 提出的 dict 中的 value
            start: int, key 在 text 中的起始下标
            end: int, key 在 text 中结束下标
        '''

        results = []
        for index, item in self._actree.iter(text):
            result = (item, index + 1 - len(item[0]), index + 1)
            results.append(result)
        return results

    def __call__(self, text):
        '''
        见 self.extract
        '''
        return self.extract(text)


if __name__ == "__main__":
    import time
    ke = KeywordExtractor(user_dict={'花呗': {'type':'biz'}, '还款': {'type':'act'}})
    while True:
        sentence = input("\nINPUT : ")
        ss = time.time()
        res = ke(sentence)
        print("TIME  : {0}ms!". format(round(1000*(time.time() - ss), 3)))
        print("OUTPUT:{0}".format(res))

```