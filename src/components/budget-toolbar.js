import Image from "next/image";
import MinimalCalendar from "./minimal-calendar";
import BudgetToolBarActions from "./budet-toolbar-actions";

export default function BudgetToolBar() {
    return (
        <div className="budget-toobar">
            <MinimalCalendar />
            <BudgetToolBarActions>
                
            </BudgetToolBarActions>
        </div>
    )
}
