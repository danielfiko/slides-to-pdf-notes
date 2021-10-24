import PyPDF2 as pdf    # pakke som behandler pdfer
from os import listdir  # brukes for å liste alle filene i mappen


def convert_to_landscape(fn):                               # funksjonen som endrer pdfene
    input1 = pdf.PdfFileReader(open(fn, "rb"))              # leser inn pdfen som skal endres
    output = pdf.PdfFileWriter()                            # oppretter den nye pdfen

    number_pages = input1.getNumPages()                     # teller antall sider i pdfen vi endrer
    for pn in range(number_pages):                          # looper gjennom alle sidene i pdfen
        input2 = pdf.PdfFileReader(open("dots.pdf", "rb"))  # leser inn dot-bakgrunnen
        print(str(pn + 1) + " av " + str(number_pages))     # printer ut hvor langt vi har kommet
        page = input1.getPage(pn)                           # velger nåværende side i fila vi skal endre
        dots = input2.getPage(0)                            # henter inn dot-bakgrunnen
        # regner ut hvor mye fila skal krympes
        scale = dots.mediaBox.getUpperRight_x() / page.mediaBox.getUpperRight_x()
        # regner ut hvor mye den må flyttes
        trans_y = dots.mediaBox.getUpperRight_y() - page.mediaBox.getUpperRight_y() * scale
        # slår sammen siden vi skal endre og dot-bakgrunnen, krymper og flytter pdfen til toppen av siden
        dots.mergeScaledTranslatedPage(page, scale, 0, trans_y, False)
        output.addPage(dots)                                # legger siden til den nye pdfen

    out_fn = fn.replace(".pdf", str(pn) + "_notat.pdf")     # legger til "_notat" på filnavnet til den nye fila
    output.removeLinks()                                    # fjerner linker fra pdfen
    output_stream = open(out_fn, "wb")                      # åpner den nye filen på harddisken (oppretter den)
    output.write(output_stream)                             # lagrer fila

files = listdir()                                           # lager en liste over alle filer i mappa

for file in files:                                                                      # looper gjennom alle filene
    if file.lower().endswith(".pdf") and not file.endswith(("dots.pdf", "_notat.pdf")):  # sjekker at det er en pdf
        convert_to_landscape(file)                                                     # sender fila til funksjonen over
