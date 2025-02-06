import pandas as pd
from string import digits
import fitz

def count_words_in_str(long_str, keys):
    """
    It counts the sum of number of times each element in the array "keys" occurs in the string "long_str".

    Parameters
    -----------
    long_str: The long string which needs to be checked for the count of words.

    keys: The array of keys for which we need to count the occurrence of.

    Returns
    --------
    count: The sum of number of times each element in the array Keys occurs in the string "long_str"

    Sample Output:
    --------------
    count_words_in_str("vibudh rocks dh dh ddh",["vi", "dh"])
    Output: 5
    """

    count = 0
    for word in long_str.split():
        for key in keys:
            if key in word:
                count = count + 1
    return(count)


def area_of_imgblocks(imgblocks):
    """
    It adds the
    """

    sum_areas = 0
    for imgblock in imgblocks:
        block_area = imgblock['width'] * imgblock['height']
        sum_areas = sum_areas + block_area
    return(sum_areas)


def extract_features(dataIDs, path):
    words_in_page = []

    scale = []
    km_kilometers = []
    m = []
    metres = []
    scale_grp = []

    legend = []

    figure = []
    mapp = []
    alignment_sheet = []
    sheet = []
    figure_grp = []

    north = []
    n = []
    north_grp = []

    dataID_pageNo = []

    i = 0
    count = 0

    No_of_images = []
    Area_of_images = []
    cnt = 0

    page_no = []
    error_files = []

    for dataID in dataIDs:
        pdf_path = path + str(dataID) + '.pdf'
        i = i + 1  # Number of files
        print("File Starting: {}. PDF {} out of {}".format(dataID, i, len(dataIDs)))

        try:
            j = 0
            doc = fitz.open(pdf_path)

            for page in doc:  # iterate through the pages
                j = j + 1  # Number of pages
                cnt = cnt + 1
                p = page.getText("dict")

                blocks = p["blocks"]
                imgblocks = [b for b in blocks if b["type"] == 1]
                No_of_images.append(len(imgblocks))
                Area_of_images.append(area_of_imgblocks(imgblocks))

                p = str(p).replace('<p>', '').replace('</p>', '').replace(".", '').replace(",", '').replace('"',
                                                                                                      '').lower()
                remove_digits = str.maketrans('', '', digits)
                p = p.translate(remove_digits)
                words_lst = p.split()
                word_count = 0
                big_words = ""
                words = ""
                for word in words_lst:
                    words = words + " " + word
                    if len(word) > 3:
                        word_count = word_count + 1
                        big_words = big_words + " " + word

                words_in_page.append(word_count)

                sc_grp = 0
                if "scale" in big_words:
                    scale.append(count_words_in_str(big_words, ["scale"]))
                    sc_grp = 1
                else:
                    scale.append(0)

                if ("kilometre" in big_words or "kilometer" in big_words or "km " in p):
                    km_kilometers.append(count_words_in_str(p, ["kilometre", "kilometer", "km "]))
                    sc_grp = 1
                else:
                    km_kilometers.append(0)

                if ("m " in p):
                    m.append(count_words_in_str(p, "m "))
                else:
                    m.append(0)

                if ("metre" in big_words or "meter" in big_words):
                    metres.append(count_words_in_str(big_words, ["meter", "metre"]))
                    sc_grp = 1
                else:
                    metres.append(0)

                if sc_grp > 0:
                    scale_grp.append(1)
                else:
                    scale_grp.append(0)

                if "legend" in big_words:
                    legend.append(count_words_in_str(big_words, ["legend"]))
                else:
                    legend.append(0)

                fig_grp = 0
                if "figure" in big_words:
                    figure.append(count_words_in_str(big_words, ["figure"]))
                    fig_grp = 1
                else:
                    figure.append(0)

                if "map " in p:
                    mapp.append(count_words_in_str(p, ["map "]))
                    fig_grp = 1
                else:
                    mapp.append(0)

                if "alignment sheet" in big_words:
                    alignment_sheet.append(1)
                    fig_grp = 1
                else:
                    alignment_sheet.append(0)

                if "sheet" in big_words:
                    sheet.append(count_words_in_str(big_words, ["sheet"]))
                    fig_grp = 1
                else:
                    sheet.append(0)

                if fig_grp > 0:
                    figure_grp.append(1)
                else:
                    figure_grp.append(0)

                if "north" in big_words:
                    north.append(count_words_in_str(big_words, ["north"]))
                    no_grp = 1
                else:
                    north.append(0)

                if "n" in p:
                    n.append(count_words_in_str(p, [" n "]))
                    no_grp = 1
                else:
                    n.append(0)

                dataID_pageNo.append(str(dataID) + "_" + str(j))
            page_no.append(j)

        except:
            print("Error Found")
            error_files.append(dataID)
            page_no.append(j)

    Features = pd.DataFrame({'scale': scale,
                             'km_kilometers': km_kilometers,
                             'm': m,
                             'metres': metres,
                             'scale_grp': scale_grp,
                             'legend': legend,
                             'figure': figure,
                             'mapp': mapp,
                             'alignment_sheet': alignment_sheet,
                             'sheet': sheet,
                             'figure_grp': figure_grp,
                             'north': north,
                             'n': n,
                             'words_in_page': words_in_page,
                             'No_of_images': No_of_images,
                             'Area_of_images': Area_of_images,
                             'dataID_pageNo': dataID_pageNo,
                             # 'Y_class' : Y_class
                             })
    DataIDs = pd.DataFrame({'DataIDs': dataIDs,
                            'Page_no': page_no})

    # print("Total Number of pages processed: {}".format(count))
    return Features, DataIDs, error_files