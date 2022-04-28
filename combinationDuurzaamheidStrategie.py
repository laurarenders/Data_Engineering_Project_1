import pathlib
import fitz
import re

websitefiles = "./contents"
reportfiles = "./annualReports"
count = 0
mogelijkeCombi = False
aantalVoorkomens = 1

# Websitecontent overlopen en scannen op duurzaamheid en strategie
for path in pathlib.Path(websitefiles).iterdir():
  aantalVoorkomens = 1
  file = open(path, "r")
  ondernemingsnr = str(path).split("\\")[1].split(".")[0]
  
  content = file.read()

  words = content.split(" ")
  for word in words:
    word = word.lower()
    if "duurza" in word:
      mogelijkeCombi = True
    

    if mogelijkeCombi:
      if count <= 50:
        if "strateg" in word:
          print(str(ondernemingsnr))
          result = open("resultaatWebsitecontent", "a+")
          if aantalVoorkomens == 1:
            result.write("\n")
          result.write(str(ondernemingsnr))
          result.write(f"\t{aantalVoorkomens}\n")
          result.close()
          aantalVoorkomens += 1
        count += 1
      
      else:
        mogelijkeCombi = False
        count = 0
  
  for word in words:
    word = word.lower()
    if "strateg" in word:
      mogelijkeCombi = True
    

    if mogelijkeCombi:
      if count <= 50:
        if "duurza" in word:
          result = open("resultaatWebsitecontent", "a+")
          if aantalVoorkomens == 1:
            result.write("\n")
          print(str(ondernemingsnr))
          result.write(str(ondernemingsnr))
          result.write(f"\t{aantalVoorkomens}\n")
          result.close()
          aantalVoorkomens += 1
        count += 1
      
      else:
        mogelijkeCombi = False
        count = 0

  file.close()
  

# Reportcontent overlopen en scannen op duurzaamheid en strategie
pattern = re.compile("[0-9]{4}\.{1}[0-9]{3}\.{1}[0-9]{3}")
for path in pathlib.Path(reportfiles).iterdir():
  aantalVoorkomens = 1
  file = fitz.open(path)
  content = ""
  for page in file:
    content += page.get_text()
  
  words = content.split(" ")

  # Search for companynumber
  for word in words:
    if pattern.match(word):
      ondernemingsnr = word.split(".")[0] + word.split(".")[1] + word.split(".")[2].split("\n")[0]

  for word in words:
    word = word.lower()
    if "duurza" in word:
      mogelijkeCombi = True
    

    if mogelijkeCombi:
      if count <= 50:
        if "strateg" in word:
          print(str(ondernemingsnr))
          result = open("resultaatReportcontent", "a+")
          if aantalVoorkomens == 1:
            result.write("\n")
          result.write(str(ondernemingsnr))
          result.write(f"\t{aantalVoorkomens}\n")
          result.close()
          aantalVoorkomens += 1
        count += 1
      
      else:
        mogelijkeCombi = False
        count = 0
  
  for word in words:
    word = word.lower()
    if "strateg" in word:
      mogelijkeCombi = True
    

    if mogelijkeCombi:
      if count <= 50:
        if "duurza" in word:
          result = open("resultaatReportcontent", "a+")
          if aantalVoorkomens == 1:
            result.write("\n")
          print(str(ondernemingsnr))
          result.write(str(ondernemingsnr))
          result.write(f"\t{aantalVoorkomens}\n")
          result.close()
          aantalVoorkomens += 1
        count += 1
      
      else:
        mogelijkeCombi = False
        count = 0
  
  file.close()

print("end")
