import Image from "next/image";
import './navbar-elm.css';

export default function NavBarElm({ src }) {
    return (
        <button className="nav-button">
            <Image src={src} height={24} width={24}/>
        </button>
    )
}
