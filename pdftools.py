from urlvalidator import UrlValidator

import pikepdf

class PdfTools:
    @staticmethod
    def removeUrlTextElements(pdfPath: str, outputPath: str, targetText: str = None):
        """移除PDF中的URL文本元素（或指定文本内容的元素）
        
        """
        with pikepdf.Pdf.open(pdfPath) as pdf:
            for pageIdx in range(len(pdf.pages)):
                page = pdf.pages[pageIdx]

                # 获取页面内容流
                if '/Contents' not in page:
                    continue
                contents = page['/Contents']

                if isinstance(contents, pikepdf.Stream): # 单个内容流
                    contentText = contents.read_bytes().decode('utf-8', errors='ignore')
                    if targetText is None:
                        if UrlValidator.validUrl(contentText):
                            del page['/Contents']
                    elif targetText in contentText:
                        del page['/Contents']
                elif isinstance(contents, pikepdf.Array): # 多个内容流
                    newContents = []
                    for content in contents:
                        if isinstance(content, pikepdf.Stream):
                            contentText = content.read_bytes().decode('utf-8', errors='ignore')
                            if targetText is None:
                                if not UrlValidator.validUrl(contentText):
                                    newContents.append(content)
                            elif targetText not in contentText:
                                newContents.append(content)
                    
                    if newContents:
                        page['/Contents'] = pikepdf.Array(newContents)
                    else:
                        del page['/Contents']

            pdf.save(outputPath)

def test():
    pdfPath = 'GBT 4460-2013 机械制图 机构运动简图用图形符号.pdf'
    outputPath = 'GBT 4460-2013 机械制图 机构运动简图用图形符号 (no url).pdf'
    PdfTools.removeUrlTextElements(pdfPath, outputPath)

if __name__ == '__main__':
    test()