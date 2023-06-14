import BudgetNavBarMain from "./budget-navbar-main";
import NavBarElm from "./navbar-elm";
import "./budget-navbar.css";

export default function BuddgetNavBar() {
  return (
    <nav className="budget-navbar">
      <BudgetNavBarMain>
        <NavBarElm src="/budget_icon.svg" />
        <NavBarElm src="/budget_icon.svg" />
        <NavBarElm src="/reports_icon.svg" />
        <NavBarElm src="/accounts_icon.svg"/>
        <NavBarElm src="/receipt_icon.svg"/>
      </BudgetNavBarMain>
    </nav>
  );
}
