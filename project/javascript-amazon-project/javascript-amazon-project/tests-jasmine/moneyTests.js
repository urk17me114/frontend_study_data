import { formatCurrency } from "../scripts/utils/money.js";   

describe("Testsuite: Format currency",()=>{
    it(" Test case 1: converts cents into dollars",()=>{
        expect(formatCurrency(2095)).toEqual("20.95");
        });
    
    it(("Test case 2: Works with 0"),()=>{
        expect(formatCurrency(0)).toEqual("0.00");
    });
    
    it(("Test case 3: Rounds up to the nearest cent"),()=>{
        expect(formatCurrency(2000.5)).toEqual("20.00");
    });
    
    });

 