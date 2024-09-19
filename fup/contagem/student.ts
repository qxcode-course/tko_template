import { write } from "fs";

function count(vet: number[], value: number): number {
    let count = 0;
    for (let elem of vet) {
        if (elem == value) {
            count += 1
        }
    }
    return count;
}

function sum(vet: number[]): number {
    let total = 0;
    for (let elem of vet) {
        total += Math.abs(elem);
    }
    return total;
}

function average(vet: number[]): number {
    return sum(vet) / vet.length;
}

function more_men(vet: number[]): string {
    let men: number[] = vet.filter(x => x > 0);
    let women: number[] = vet.filter(x => x < 0);
    let average_men = average(men);
    let average_women = average(women);

    if (average_men == average_women) {
        return "draw";
    }
    if (average_men > average_women) {
        return "men";
    }
    return "women";
}

function half_compare(vet: number[]): string {
    let half = vet.length / 2
    let first: number[] = vet.slice(0, half);
    // for (let i = 0; i < half; i++) {
    //     first.push(vet[i]);
    // }
    let second: number[] = vet.slice(half, vet.length);
    // for (let i = half; i < vet.length; i++) {
    //     second.push(vet[i]);
    // }
    
    return "";
}

function sex_battle(vet: number[]): string {


    return "";
}

if (require.main === module) {
}

export { count, sum, average, more_men, half_compare, sex_battle };