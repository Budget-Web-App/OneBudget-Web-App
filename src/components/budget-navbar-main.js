import { Children, cloneElement } from "react";
import './budget-navbar-main.css';

export default function BudgetNavBarMain({ children }) {
  return (
    <div className="budget-nav-main">
      <ul>
        {Children.map(Children.toArray(children), (child, index) => (
          <li key={index}>{child}</li>
        ))}
      </ul>
    </div>
  );
}
