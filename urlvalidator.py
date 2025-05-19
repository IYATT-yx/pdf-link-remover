import re

class UrlValidator:
    @staticmethod
    def _containsIpv4(text: str) -> bool:
        ipv4Pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return re.search(ipv4Pattern, text) is not None
    
    @staticmethod
    def _containsIpv6(text: str) -> bool:
        ipv6Pattern = r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'
        return re.search(ipv6Pattern, text) is not None
    
    @staticmethod
    def _containsDomain(text: str) -> bool:
        domainPattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        return re.search(domainPattern, text) is not None
    
    @staticmethod
    def _containsUrl(text: str) -> bool:
        urlPattern = r'\bhttps?://[^\s]+'
        return re.search(urlPattern, text) is not None

    
    @staticmethod
    def validUrl(text: str) -> bool:
        """验证是否包含了 URL

        Args:
            text (str): 待验证的字符串

        Returns:
            bool: 是否为 URL
        """
        if UrlValidator._containsIpv4(text):
            return True
        elif UrlValidator._containsIpv6(text):
            return True
        elif UrlValidator._containsDomain(text):
            return True
        elif UrlValidator._containsUrl(text):
            return True
        return False
    
def test():
    texts = [
        '127.0.0.1',
        'http://127.0.0.1',
        'https://127.0.0.1',
        'www.baidu.com',
        'http://www.baidu.com',
        'https://www.baidu.com',
        'https://asadsad',
        'http://adsdasd'
        'dasdasdas.dasds',
        'http://dasd.dasds',
        'daasfaf',
        '3434.5345',
        '423423.com'
    ]

    for text in texts:
        print(f'{UrlValidator.validUrl(text)} {text}')

if __name__ == "__main__":
    test()