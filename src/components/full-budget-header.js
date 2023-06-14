import Image from "next/image";
import './navbar-elm.css';
import BudgetToolBar from "./budget-toolbar";

export default function FullBudgetHeader() {
    return (
        <div className="full-budget-header">
            <BudgetToolBar/>
        </div>
    )
}
