#------------------------------------------------
# Basic Design
#------------------------------------------------

from wissen import Wissen

analyzer = Wissen.StandardAnalyzer () # english porter stem analyzer
indexer = Wissen.Indexer ("d:\\var\\wissen-test", analyzer)
document = Wissen.Document ()

document.addField (Wissen.TextField ("title", "Title"))
document.addField (Wissen.IntField ("isbn", 52652, 8))
document.addField (Wissen.BitField ("flags", "10011000", 8))
document.addField (Wissen.CoordField ("latlon", 34.435, 123.3434))
document.addField (Wissen.StringField ("author", "Jason Bourngh"))

document.addData ({"sadas", [1,2312,123,213,2131]})

indexer.addDocument (document)
indexer.close ()

mem = Wissen.Memory (4096)
searcher = Wissen.Searcher (mem, "d:\\var\\wissen-test", analyzer)
rset = searcher.query ("title:", 0, 5)
searcher.close ()
mem.free ()

rset["qs"]
rset["code"]
rset["time"]
rset["totalrecords"]
rset["offset"]
rset["length"]
rset["hlterms"]

for data in rset["result"]:
	print data

