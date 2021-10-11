import execjs

with open('./rsa.js', 'r') as f:
  js_code = f.read()

js_complied = execjs.compile(js_code)

def rsa_enc(content): 
  js_func = js_complied.call("strEnc", content, "1", "2", "3")
  return js_func
  
def rsa_dec(content):
  js_func = js_complied.call("strDec", content, "1", "2", "3")
  return js_func
