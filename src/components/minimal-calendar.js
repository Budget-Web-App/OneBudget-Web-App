import Image from "next/image";
import './minimal-calendar.css';

export default function MinimalCalendar() {
    return (
        <div className="minimal-calendar">
            <Image src="/left-arrow.svg" width={20} height={20}/>
            <p>June</p>
            <p>2023</p>
            <Image src="/right-arrow.svg" width={20} height={20}/>
        </div>
    )
}
