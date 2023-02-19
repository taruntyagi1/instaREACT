import React, { useEffect, useState } from "react";
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { FiShoppingCart } from "react-icons/fi";
import axios from "axios";
// import { useSelector } from "react-redux";

export default function Header() {
    const [count, setCount] = useState(0);
    const [userID, setUserID] = useState()

    const navigate = useNavigate();
    const [authstatus, setAuthStatus] = useState('logged out')
    const handlelogout = () => {
        localStorage.removeItem('data')
        navigate('/login')
    }


    const getdata = () => {
        const data = localStorage.getItem("data")
        if (data) {
            const parseData = JSON.parse(data)
            // console.log("data",parseData)
            const { id } = parseData
            setUserID(id)
        }


    }

    useEffect(() => {
        getdata();
    }, [])









    const cartcount = async () => {
        if (userID) {

            const response = await axios.get('http://127.0.0.1:8000/count/', {params : {userID}})
            console.log(response.data)
            setCount(response.data.message)
        } else {
            console.log('user id is not found')
        }




    }
    window.cartcount = cartcount;
    
    useEffect(() => {
        cartcount();
    })


    const session_cart = localStorage.getItem('cart_data')
    //convert session_cart to json.parse data
    const cart = JSON.parse(session_cart)
    console.log('user_session', cart)


    const handlesession_cart = () => {
        const response = axios.post('http://127.0.0.1:8000/session_cart/', {
            user_id: userID,cart
        })
        console.log(response.data)
        localStorage.removeItem('cart_data')
    }







    useEffect(() => {
        const data = JSON.parse(localStorage.getItem('data'))


        if (data) {
            setAuthStatus("logged in")
        } else {
            setAuthStatus('logged out')
        }

        // eslint-disable-next-line
    }, [setAuthStatus])


    return (
        <div className="header">
            <div className="container">
                <div className="nav-bar">
                    <img src="data:image/png;base64,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" alt="" />
                    <ul className="nav-item">
                        <button> <li className="nav-link"><Link to='/'>Home</Link></li></button>

                        <button><li className="nav-link">Products</li></button>
                        {authstatus === 'logged in' ? (
                            <>
                                <button><li onClick={handlelogout} className="nav-link">Logout</li></button>
                                <button><li className="nav-link"><Link to='/dashboard'>Dashboard</Link></li></button>

                            </>
                        ) : (
                            <>
                                <button><li className="nav-link"><Link to='/login'>Login</Link></li></button>
                                <button><li className="nav-link"><Link to='/register'>Register</Link></li></button>
                            </>

                        )}
                        <li id="cart_btn" onClick={handlesession_cart} className="nav-link"><Link to='/cart'><FiShoppingCart /><i>{count}</i></Link></li>
                    </ul>

                </div>
            </div>
        </div>
    )
}