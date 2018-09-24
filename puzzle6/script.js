let voter = {
    // A:[12091,18130,18601,44474,26237,72357,19450,14108,9606,3653,5056,406,17919,36553,110982,87257,19339,84163,23757,58379,30650,20983,10920,105080,19949,41919,16630,30276,8673,77294,66794,25160,13123,35890,6756,63044,18894,26162,57836,38897,79582,24349,75933,6557,32386,49254,15735,180599,17956,105401,18925,6520,2224,25364,77336,38849,21749,179283,6409,84725,4225,56712,18870,25883,93843,1798,50567,81127,72077,99987,64535,30834,5421,199544,15500,4792,2090,75186,170275,21789,3907,15930,891,2938,27300,0,21124,627,29698,385555,10567,2835,14024,23092,9823,67068,55761,83430,140754,18493],
    // B:[60473,115746,6510,45538,24577,60646,28538,13799,2909,3027,11379,872,8300,39985,62654,56773,30413,58629,45047,38706,25759,17074,41366,78805,8395,39536,13726,73682,17889,97551,60187,71356,7828,31092,48166,43077,72006,104532,59203,51552,224672,72410,23815,12868,31871,32779,22823,162812,15064,96966,67895,4960,2205,18667,34292,22763,41726,84691,15697,81677,8289,72337,39992,46004,80352,18276,220484,149292,62529,95252,131871,80950,31359,171539,78171,22334,1451,74542,144226,54712,1159,22552,8076,2115,21050,53702,62141,3793,19436,183545,10673,6067,6856,6180,26347,116035,58202,47832,70373,27511],
    // MinExpectedA: 14,
    // Imbalance: 117E10,
    // Efficiency: -0.307,
    // A: [561, 9841, 252940, 10456, 5543, 11935, 64457, 3085, 7162, 34567, 109791, 15070, 25364, 26382, 6056, 3738, 54804, 79485, 9249, 29892, 2375, 10585, 2566, 19173, 2375, 4390, 85376, 239497, 232591, 17178, 26636, 4793, 98154, 76692, 12301, 5571, 28098, 2975, 44847, 93333, 119573, 101189, 13463, 756, 14127, 37550, 16705, 52842, 68943, 165622, 19630, 47237, 46941, 42957, 5994, 17710, 33238, 1489, 129997, 22973, 83955, 11674, 46176, 61017, 158, 3757, 12447, 12270, 27250, 185716, 241, 22438, 4519, 10713, 67802, 25341, 65905, 30684, 4370, 67471, 14579, 9670, 3413, 1617, 20641, 125847, 17584, 34370, 25949, 16411, 172802, 22348, 193399, 53895, 44262, 34407, 20888, 79658, 56836, 246823],
    // B: [1422, 8050, 378822, 7428, 4711, 41567, 5377, 22826, 7361, 68097, 58264, 5719, 34365, 147437, 52002, 21856, 41969, 48539, 19416, 27884, 40126, 5706, 884, 11415, 284925, 21183, 34793, 286051, 74388, 7231, 181857, 10052, 274011, 109528, 15650, 5793, 39078, 9150, 22833, 102693, 72944, 31353, 37985, 2597, 16072, 66567, 41868, 224420, 197387, 95169, 82188, 13856, 60915, 123669, 55061, 34395, 60065, 12920, 32451, 15671, 110069, 172580, 29620, 46840, 156, 11934, 38153, 119598, 38772, 298665, 203, 154273, 13016, 66313, 84708, 26821, 109265, 13097, 25888, 288709, 27295, 14115, 2478, 3255, 55184, 179130, 36273, 3313, 50249, 43479, 154526, 66770, 117534, 68404, 131620, 13146, 13310, 73454, 38187, 213992],
    // MinExpectedA: 11,
    // Imbalance: 227E10,
    // Efficiency: -0.189,
    A:[14831,5709,3158,2257,60545,91119,5112,38892,95250,15716,325,18052,22731,33344,9055,5731,13579,25769,22224,7869,3107,79090,15025,31563,36024,3163,32002,12139,110818,4912,66080,49766,61468,577,7692,32907,4698,10971,46644,49251,9452,84134,168959,1407,4471,49961,15868,26564,44271,5138,11212,8380,41166,7774,15628,7227,575,16810,10004,8096,18284,5626,34841,32614,1960,79632,34821,32498,12406,11393,80804,10979,15900,2228,94555,22731,25433,244130,7725,72722,16049,109963,63231,160871,0,16474,4104,9740,160767,19472,16387,2481,134674,128680,7357,79945,13754,38546,34810,9691],
    B:[19685,16312,6466,13100,68391,7359,4231,57503,89884,75035,2089,14423,129543,15697,5107,22683,26107,46106,7758,13267,19185,95305,22243,11046,61655,5467,81613,42298,98993,8428,104288,48835,70801,839,15128,23008,40015,14698,50628,122359,4108,57639,168647,1339,9477,101807,31693,44236,75472,1698,79379,18534,11491,35072,46690,15461,7489,53184,67396,24831,53679,9188,14820,31240,2845,166905,72996,19804,66001,41195,40204,14542,8580,13403,91342,10155,7838,287056,20670,39874,32518,157762,194694,94415,305850,108212,10425,14616,122938,11259,105498,2012,137552,208417,102083,98967,92000,41443,47197,14246],
    MinExpectedA: 11,
    Imbalance: 205E10,
    Efficiency: -0.140,
    FavorableProbability: 0.6
};
voter.T = [];

function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

let table = {
    t: document.getElementById("blocks"),
    r: [],
    color: [],
    colorBlock: function (b, d) {
        this.r[b].style.backgroundColor = this.color[d];
    }
};
(() => {
    for (let i = 0; i < 20; i++) {
        table.color.push(getRandomColor());
    }

    for (let i = 0; i < 10; i++) {
        let r = document.createElement("tr");
        for (let j = 0; j < 10; j++) {
            let d = document.createElement("td");
            d.innerHTML = "" + (i * 10 + j);
            table.r.push(d);
            r.appendChild(d);
        }
        table.t.appendChild(r);
    }
})();

class Block {
    constructor(aVoter, bVoter, row, col, index, city) {
        this.A = aVoter;
        this.B = bVoter;
        this.population = this.A + this.B;
        this.T = this.population;
        this.win = (this.A * voter.FavorableProbability + this.B * (1 - voter.FavorableProbability)) / this.T;
        this.row = row;
        this.col = col;
        this.index = index;
        this.city = city;
        this.district = null;
    }
    setDistrict(district){
        this.district = district;
        if (this.district)
            table.colorBlock(this.index, this.district.index);
    }
    update(){
        this.S = this.row === 0 ? null : this.city.getBlock(this.row - 1, this.col);
        this.X = this.row === 9 ? null : this.city.getBlock(this.row + 1, this.col);
        this.Z = this.col === 0 ? null : this.city.getBlock(this.row, this.col - 1);
        this.C = this.col === 9 ? null : this.city.getBlock(this.row, this.col + 1);
    }
    howDetachable(){
        let a = new Set();
        a.add(this.district);
        a.add(this.S ? this.S.district : null);
        a.add(this.Z ? this.Z.district : null);
        a.add(this.X ? this.X.district : null);
        a.add(this.C ? this.C.district : null);
        a.delete(null);
        return Array.from(a);
    }
}
class Districts {
    constructor(index, city) {
        this.blocks = new Set();
        this.index = index;
        this.city = city;
    }
    get population(){
        let p = 0;
        this.blocks.forEach(function (i) {
            p += i.population;
        });
        return p;
    }
    get win(){
        if(this.blocks.size === 0){
            return 0;
        }
        let aVoter = 0;
        let bVoter = 0;
        this.blocks.forEach(function (i) {
            aVoter += i.A;
            bVoter += i.B;
        });
        return (aVoter * voter.FavorableProbability + bVoter * (1 - voter.FavorableProbability)) / (aVoter + bVoter);
    }
    get aVotes(){
        if(this.blocks.size === 0){
            return 0;
        }
        let aVoter = 0;
        let bVoter = 0;
        this.blocks.forEach(function (i) {
            aVoter += i.A;
            bVoter += i.B;
        });
        return (aVoter * 0.6 + bVoter * 0.4);
    }
    get bVotes(){
        return this.population - this.aVotes;
    }
    isWinning(){
        return this.win > 0.5
    }
    transfer(block){
        let pre = block.district;
        if(pre === this){
            return true;
        }
        try {
            if(this.transferAble(block)){
                block.district.blocks.delete(block);
                this.blocks.add(block);
                block.setDistrict(this);
                return true;
            } else {
                return false;
            }
        } catch (e) {
            return false;
        }
    }
    transferAble(block){
        let pre = block.district;
        if(pre === this){
            return true;
        }
        try {
            block.setDistrict(null);
            pre.blocks.delete(block);
            let r = pre.isContinuous();
            block.setDistrict(this);
            this.blocks.add(block);
            r = r && this.isContinuous();
            this.blocks.delete(block);
            block.setDistrict(pre);
            pre.blocks.add(block);
            return r;
        } catch (e) {
            return false;
        }
    }
    isContinuous(){
        function eqSet(as, bs) {
            if (as.size !== bs.size) return false;
            for (let a of as) if (!bs.has(a)) return false;
            return true;
        }

        if(this.blocks.size > 0) {
            let s = new Set();
            let c = new Set();
            let que = [this.blocks.values().next().value];
            while (que.length > 0) {
                let x = que.pop();
                if (c.has(x)){
                    continue;
                } else {
                    c.add(x);
                }
                if (x && x.district === this) {
                    s.add(x);
                    if (!c.has(x.S)) { que.push(x.S); }
                    if (!c.has(x.X)) { que.push(x.X); }
                    if (!c.has(x.Z)) { que.push(x.Z); }
                    if (!c.has(x.C)) { que.push(x.C); }
                }
            }
            return eqSet(this.blocks, s);
        } else {
            return false;
        }
    }
    reset(){
        this.blocks.forEach(function (i) {
            i.setDistrict(null);
        });
        this.blocks.clear();
    }
}
class City {
    constructor() {
        this.blocks = [];
        this.vBlocks = [];
        for (let i = 0; i < 10; i++) {
            this.vBlocks.push([]);
        }
        this.districts = [];
        for (let i = 0; i < 20; i++) {
            this.districts.push(new Districts(i, this));
        }
        for (let i = 0; i < 100; i++) {
            let b = new Block(voter.A[i], voter.B[i], Math.floor(i / 10), i % 10, i, this);
            this.blocks.push(b);
            this.vBlocks[Math.floor(i / 10)][i % 10] = b;
        }
        for (let i = 0; i < 100; i++) {
            this.blocks[i].update();
        }
    }
    get totalPopulation(){
        let p = 0;
        for (let i = 0; i < this.districts.length; i++) {
            p += this.districts[i].population;
        }
        return p;
    }

    get expectedWin(){
        let win = 0;
        for (let i = 0; i < this.districts.length; i++) {
            win += this.districts[i].win;
        }
        return win;
    }
    get expectedWholeWin(){
        let win = 0;
        for (let i = 0; i < this.districts.length; i++) {
            win += this.districts[i].win > 0.5 ? 1 : 0;
        }
        return win;
    }
    get imbalance() {
        let meanPopulation = this.totalPopulation / 20;
        let imbalance = 0;
        for (let i = 0; i < this.districts.length; i++) {
            imbalance += Math.pow(meanPopulation - this.districts[i].population, 2)
        }
        return imbalance;
    }
    get efficiency() {
        let wastedVoteA = 0;
        let wastedVoteB = 0;
        for (let i = 0; i < this.districts.length; i++) {
            if (this.districts[i].isWinning()){
                wastedVoteA += this.districts[i].aVotes - (Math.floor(this.districts[i].population / 2) + 1);
                wastedVoteB += this.districts[i].bVotes;
            } else {
                wastedVoteA += this.districts[i].aVotes;
                wastedVoteB += this.districts[i].bVotes - (Math.floor(this.districts[i].population / 2) + 1);
            }
        }
        return (wastedVoteA - wastedVoteB) / this.totalPopulation;
    }

    get lossExpectedWin(){
        return Math.pow(this.expectedWin * 2 - this.districts.length, 3);
    }
    get lossExpectedWholeWin(){
        return Math.tanh(((this.expectedWholeWin + this.lossExpectedWin / 2) - (voter.MinExpectedA + 1)) / (voter.MinExpectedA + 1));
    }
    get lossImbalance(){
        return Math.tanh((voter.Imbalance - this.imbalance) / voter.Imbalance)
    }
    get lossEfficiency(){
        return Math.tanh((this.efficiency - voter.Efficiency) / Math.abs(voter.Efficiency))
    }
    get lossGrid() {
        return [
            // this.lossExpectedWholeWin +this.lossImbalance,
            // this.lossExpectedWholeWin +this.lossImbalance,
            this.lossExpectedWholeWin,
            this.lossImbalance,
            this.lossEfficiency,
        ];
    }
    get loss(){
        return Math.min(...this.lossGrid);
    }

    get isOK(){
        return this.loss > 0;
    }

    getBlock(row, col){
        return this.vBlocks[row][col];
    }

    isDistributionValid(){
        let c = true;
        this.districts.forEach(function (i) {
            c = c && i.isContinuous();
        });
        return c;
    }
    setDistribution (distribution) {
        for (let i = 0; i < this.districts.length; i++) {
            this.districts[i].reset()
        }
        for (let i = 0; i < distribution.length; i++) {
            for (let j = 0; j < distribution[i].length; j++) {
                this.blocks[distribution[i][j]].setDistrict(this.districts[i]);
                this.districts[i].blocks.add(this.blocks[distribution[i][j]]);
            }
        }
        if(!this.isDistributionValid()){
            this.districts.forEach(function (i) {
                i.reset();
            });
        }
    }
    getDistribution(){
        let x = [];
        let i;
        for (i = 0; i < this.districts.length; i++) {
            x[i] = [];
        }
        for (i = 0; i < this.blocks.length; i++) {
            x[this.blocks[i].district.index].push(i);
        }
        return x;
    }
    getDistributionJSON(){
        return JSON.stringify(this.getDistribution());
    }
}

let city = new City();
city.setDistribution([
    [0, 1, 10, 11, 20],
    [2, 3, 12, 13, 22],
    [4, 5, 14, 15, 24],
    [6, 7, 16, 17, 26],
    [8, 9, 18, 19, 28],
    [21, 30, 31, 40, 41],
    [23, 32, 33, 42, 43],
    [25, 34, 35, 44, 45],
    [27, 36, 37, 46, 47],
    [29, 38, 39, 48, 49],
    [50, 51, 60, 61, 70],
    [52, 53, 62, 63, 72],
    [54, 55, 64, 65, 74],
    [56, 57, 66, 67, 76],
    [58, 59, 68, 69, 78],
    [71, 80, 81, 90, 91],
    [73, 82, 83, 92, 93],
    [75, 84, 85, 94, 95],
    [77, 86, 87, 96, 97],
    [79, 88, 89, 98, 99],
]);
// city.setDistribution([[0,1,2,3,10,12,20,30,40,50,51,60,61,71,80,81,90],[13],[5],[28],[6,9,16,17,19,27,29,37,38,39,48,49,57,58,59,68,69,78],[31,32,41],[11,21,22,23],[35,43,44,45,53,62,63,72,82],[4,14,15,24,25,26,33,34,36,46,47,54,55,56,64,65],[7,8,18],[70],[42],[52],[66,67,74,75,76],[79],[91,92,93],[73,83,84,85,86,87],[77],[89,94,95,96,97,98,99],[88]]);

setInterval(function () {
    document.getElementById('stat1_o').innerHTML = voter.MinExpectedA + "";
    document.getElementById('stat1_').innerHTML = city.expectedWholeWin;
    document.getElementById('stat1_s').innerHTML = city.lossExpectedWholeWin;
    document.getElementById('stat1_d').innerHTML = "" + (city.expectedWholeWin - voter.MinExpectedA);

    document.getElementById('stat2o').innerHTML = voter.Imbalance + "";
    document.getElementById('stat2').innerHTML = city.imbalance;
    document.getElementById('stat2s').innerHTML = city.lossImbalance;
    document.getElementById('stat2d').innerHTML = "" + (voter.Imbalance - city.imbalance);

    document.getElementById('stat3o').innerHTML = voter.Efficiency + "";
    document.getElementById('stat3').innerHTML = city.efficiency;
    document.getElementById('stat3s').innerHTML = city.lossEfficiency;
    document.getElementById('stat3d').innerHTML = "" + (city.efficiency - voter.Efficiency);

    document.getElementById('loss').innerHTML = city.loss;
}, 100);

function compareParameters(arr, k = -1){
    let i = 0;
    let max = -3;
    for (let j = 0; j < Math.floor(city.lossGrid.length / 2) + 1; j++) {
        k = getRandomInt(0, city.lossGrid.length - 1);
        if (city.lossGrid[k] < 0){
            break
        }
    }
    for (let j = 0; j < arr.length; j++) {
        if(max < arr[j].lossGrid[k]){
            max = arr[j].lossGrid[k];
            i = j;
        }
    }
    return arr[i];
}

function checkBestBlockLocation(blockIndex) {
    let testArray = city.blocks[blockIndex].howDetachable();

    let statArr = [];
    let original = city.blocks[blockIndex].district;
    statArr.push({
        block: city.blocks[blockIndex],
        district: city.blocks[blockIndex].district,
        lossGrid: city.lossGrid
    });
    for (let i = 0; i < testArray.length; i++) {
        if (testArray[i].transfer(city.blocks[blockIndex])) {
            statArr.push({
                block: city.blocks[blockIndex],
                district: city.blocks[blockIndex].district,
                lossGrid: city.lossGrid
            });
        }
    }
    original.transfer(city.blocks[blockIndex]);
    return compareParameters(statArr);
}
(() => {
    let x = checkBestBlockLocation(getRandomInt(0, 99));
    x.district.transfer(x.block);
    x = checkBestBlockLocation(getRandomInt(0, 99));
    x.district.transfer(x.block);
    x = checkBestBlockLocation(getRandomInt(0, 99));
    x.district.transfer(x.block);
    x = checkBestBlockLocation(getRandomInt(0, 99));
    x.district.transfer(x.block);
    x = checkBestBlockLocation(getRandomInt(0, 99));
    x.district.transfer(x.block);
})();
function update(){
    let arr = [];
    for (let i = 0; i < city.blocks.length; i++) {
        arr.push(checkBestBlockLocation(i));
    }
    let x = compareParameters(arr);
    if(x.district === x.block.district){
        let x = checkBestBlockLocation(getRandomInt(0, 99));
        x.district.transfer(x.block)
    } else {
        x.district.transfer(x.block)
    }
    if (city.isOK) {
        document.getElementById("result").value = city.getDistributionJSON();
    } else {
        setTimeout(update, 1)
    }
}
console.log(city);
update();
