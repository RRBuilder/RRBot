from random import randrange

def PassProcess(Count, UniCode):
  List = []
  Pass = ""
  if UniCode == "1" or UniCode == "yes" or UniCode == "Yes":
    for x in range(Count-10):
      Char = randrange(31,55296)
      List.append(Char)
    for x in range(10):
      Char = randrange(31,126)
      List.append(Char)
  else:
    for x in range(Count):
      Char = randrange(31,126)
      List.append(Char)

  for x in range(len(List)):
    PassChar = chr(List[x])
    Pass = Pass + PassChar
  return Pass
