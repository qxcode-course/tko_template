var readlineSync = require('readline-sync');
let input = () : string => readlineSync.question();
let write = (text: any, end:string="\n")=> process.stdout.write("" + text + end);

let numero = Math.floor(Math.random() * 100) + 1;

let inferior = 0
let superior = 100
for (;;) {
    write(`Chute um número entre ]${inferior} e ${superior}[: `, "");
    let chute = +input()
    if (chute == numero) {
        write("Voce acertou");
        break;
    }
    if (numero < chute) { 
        superior = chute;
        write("É menor")
    }
    else{
        inferior = chute;
        write("É maior")
    }
    if (superior - inferior == 2) {
        write("você perdeu");
        break;
    }
}