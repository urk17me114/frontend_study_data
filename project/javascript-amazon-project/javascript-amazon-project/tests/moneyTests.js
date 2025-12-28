import { formatCurrency } from "../scripts/utils/money.js";    


console.log("Testsuite: Format currency");

        /*Test case 1: converts cents into dollars */
        if(formatCurrency(2095)==="20.95"){
            console.log("Test case 1 passed");}
        else{
            console.log("Test case 1 failed");
        }

        /* Test case 2 */
        if (formatCurrency(0)==="0.00"){
            console.log("Test case 2 passed");
        }
        else{
            console.log("Test case 3 failed");
        }

        /* Test case 3 */
        if (formatCurrency(2000.5)==="20.01"){
            console.log("Test case 3 passed");
        }
        else{
            console.log("Test case 3 failed");
            console.log("output is " + formatCurrency(2000.5));
        }


        