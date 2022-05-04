import asyncio
from pyppeteer import launch
from PyPDF2 import PdfFileMerger

async def cover():
    '''
    This method will be responsible for generating first page / cover page.
    '''
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://github.com/') # provide cover page url
    await page.pdf({
        'path': 'cover.pdf',
        'margin': { 'bottom': '1.44in', 'top':'0.75in', 'right': '0.52in', 'left':'0.75in' },
        'pageRanges':'1'
    })

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print("✅ Cover pdf generated")
    # print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

async def main():
    '''
    This method will generate main body part with header/footer.
    '''
    merger = PdfFileMerger()
    browser1 = await launch()
    page2 = await browser1.newPage()
    
    await page2.goto('https://github.com/puppeteer/puppeteer') # url of body pages
    await page2.pdf({
        'path': 'main.pdf',
        'displayHeaderFooter':True,
        'footerTemplate': "<div style='border-top: solid 1px #bbb; width: 100%; font-size: 9px; padding: 5px 5px 0; color: #bbb; position: relative;'> <div style='position: absolute; left: 5px; top: 5px;'><span class='date'></span></div> <div style='position: absolute; right: 5px; top: 5px;'><span class='pageNumber'></span>/<span class='totalPages'></span></div></div>",
        'margin': { 'bottom': '1.44in', 'top':'0.75in', 'right': '0.52in', 'left':'0.75in' },
        'pageRanges':'2-'
    })


    dimensions = await page2.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print("✅ Body pdf generated")
    # print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser1.close()





asyncio.get_event_loop().run_until_complete(cover())

asyncio.get_event_loop().run_until_complete(main())

'''
And finaly PdfFileMerger will merge those two pdfs and will generate final pdf.
'''
merger = PdfFileMerger()

# name of both cover and body files
for pdf in ["cover.pdf", "main.pdf"]:
    merger.append(pdf)

merger.write("merged-pdf.pdf")
print("✅ Merged pdf generated")
merger.close()