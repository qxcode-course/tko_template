let _cin_ : string[] = [];
try { _cin_ = require("fs").readFileSync(0).toString().split(/\r?\n/); } catch(e){}
let input = () : string => _cin_.length === 0 ? "" : _cin_.shift()!;
let write = (text: any, end:string="\n")=> process.stdout.write("" + text + end);
export {};

class Jogador {
    a: number;
    b: number;
    
    constructor(A: number, B: number) {
        this.a = A;
        this.b = B;
    }
    
}

function pontuacao(jogador: Jogador) : number {
    return Math.abs(jogador.a - jogador.b);
}

let qtd: number = +input();

let jogadas: Jogador[] = []

for (let i = 0; i < qtd; i++) {
    let jogador = new Jogador(0, 0);
    [jogador.a, jogador.b] = input().split(" ").map(Number); [12, 13]
    jogadas.push(jogador);
}
let ref: number = -1;
for (let i = 0; i < qtd; i++) {
    if (jogadas[i].a >= 10 && jogadas[i].b >= 10) {
        if (ref == -1) {
            ref = i;
        } else if (pontuacao(jogadas[i]) <= pontuacao(jogadas[ref])) {
            ref = i;
        }
    }
}
if (ref == -1) {
    write("sem ganhador");
} else {
    write(ref);
}
