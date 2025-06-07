from urlvalidator import UrlValidator

import pikepdf
import re


class PdfTools:
    textPattern = re.compile(r'\((.*)\)')

    @staticmethod
    def findAndClearObjectText(pdfPath: str, outputPath: str, searchText: str=None):
        with pikepdf.open(pdfPath, allow_overwriting_input=True) as pdf:
            clearObjText = []
            for idx, obj in enumerate(pdf.objects):
                if isinstance(obj, pikepdf.Stream):
                    clearFlag = False
                    try:
                        if '/Filter' in obj:
                            data = obj.read_bytes()
                        else:
                            data = obj.read_raw_bytes()
                        data = data.decode('utf-8', errors='ignore')
                        if searchText is None:
                            texts = PdfTools.textPattern.findall(data)
                            if texts == []:
                                continue

                            for text in texts:
                                if UrlValidator.validUrl(text):
                                    clearFlag = True
                                    break
                        else:
                            if searchText in data:
                                clearFlag = True
                            else:
                                continue

                        if clearFlag:
                            clearObjText.append((idx, data))
                            newText = data.replace(searchText, '') if searchText else data.replace(text, '')
                            newTextEncoded = newText.encode('utf-8', errors='ignore')
                            obj.write(newTextEncoded)
                    except pikepdf.PdfError as e:
                        # 尝试读取不支持的压缩过滤器时跳过
                        if 'read_bytes called on unfilterable stream' in str(e):
                            continue
                        else:
                            raise e
                    except Exception as e:
                        return False, f'无法处理对象 {idx} 的内容: {e}'
            pdf.save(outputPath)
            return True, clearObjText

# 这个方案只适合处理没有压缩的链接文本
#############################################################################################
# class PdfTools:
#     @staticmethod
#     def removeUrlTextElements(pdfPath: str, outputPath: str, targetText: str = None):
#         """移除PDF中的URL文本元素（或指定文本内容的元素）
        
#         """
#         with pikepdf.Pdf.open(pdfPath) as pdf:
#             for pageIdx in range(len(pdf.pages)):
#                 page = pdf.pages[pageIdx]

#                 # 获取页面内容流
#                 if '/Contents' not in page:
#                     continue
#                 contents = page['/Contents']

#                 if isinstance(contents, pikepdf.Stream): # 单个内容流
#                     contentText = contents.read_bytes()
#                     if targetText is None:
#                         if UrlValidator.validUrl(contentText):
#                             del page['/Contents']
#                     elif targetText.encode('utf-8') in contentText:
#                         del page['/Contents']
#                 elif isinstance(contents, pikepdf.Array): # 多个内容流
#                     newContents = []
#                     for content in contents:
#                         if isinstance(content, pikepdf.Stream):
#                             contentText = content.read_bytes().decode('utf-8', errors='ignore')
#                             if targetText is None:
#                                 if not UrlValidator.validUrl(contentText):
#                                     newContents.append(content)
#                             elif targetText.encode('utf-8') not in contentText:
#                                 newContents.append(content)
                    
#                     if newContents:
#                         page['/Contents'] = pikepdf.Array(newContents)
#                     else:
#                         del page['/Contents']

#             pdf.save(outputPath)
###################################################################################################
