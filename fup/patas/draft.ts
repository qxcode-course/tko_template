let _cin_ : string[] = [];
try { _cin_ = require("fs").readFileSync(0).toString().split(/\r?\n/); } catch(e){}
let input = () : string => _cin_.length === 0 ? "" : _cin_.shift()!;
let write = (text: any, end:string="\n")=> process.stdout.write("" + text + end);
export {};


ler valores
total = 0
laco qtd
  ler animal
  if vaca
    total += 4
  ...
distCB = cb - total
distCB = Math.abs(distCB)