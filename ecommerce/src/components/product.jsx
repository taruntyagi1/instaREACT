// import React, { useEffect, useState } from 'react'
// import { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Button } from "react-bootstrap";
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
// import { Add } from './action';

import { useEffect,useState } from 'react';









export default function Product(props) {
  const [user_id,setUserId] = useState('')
  //eslint-disable-next-line
  const dispatch = useDispatch();
  const [loggedIN,setLoggedIN] = useState(false)
  const data1 = JSON.parse(localStorage.getItem('data'))
  const navigate = useNavigate();
  const price = props.price
  console.log(price)
  

  
  

  useEffect(()=>{
    if(data1){
      const {id} = data1
      setUserId(id)
    } else{
      setUserId('')
    }
    if(user_id){
      setLoggedIN(true)
    }else{
      setLoggedIN(false)
    }
    
//eslint-disable-next-line
  },[data1,loggedIN])
  
  const addToCart = async()=>{
    if(loggedIN){

      const response = await axios.post(`http://127.0.0.1:8000/add/${props.id}/`,{
        user_id,price
      })
      window.cartcount();
      console.log(response.data.message)
     
  
        
      
      }else{
        let sessionCart = JSON.parse(localStorage.getItem('cart_data')) || {}

    if(sessionCart[props.id]){
      sessionCart[props.id]["quantity"] += 1;
      sessionCart[props.id]['price'] = sessionCart[props.id]['price'] * sessionCart[props.id]['quantity']
    }else{
      sessionCart[props.id] = {
        id : props.id,
        quantity: 1,
        price: price,
        image : props.image,
        title : props.title
      
      };
    }
    localStorage.setItem("cart_data", JSON.stringify(sessionCart));
      }
    }
  //   const session_cart = localStorage.getItem('cart_data')
  // //convert session_cart to json.parse data
  // const cart = JSON.parse(session_cart)
  // console.log('user_session',cart)

  //   const handlesession_cart =()=>{
  //     const response = axios.post('http://127.0.0.1:8000/session_cart/',{
  //       user_id,cart
  //     })

  //     console.log(response.data)
  //   }

  //   useEffect(()=>{
  //     if(loggedIN && user_id){
  //       handlesession_cart();
  //     }
  //     //eslint-disable-next-line
  //   },[user_id,loggedIN])
    

    // const handlesession_cart =async()=>{
    //   const response = await axios.post('http://127.0.0.1:8000/session_cart/',{
    //     user_id,cart
    //   })
    //   console.log('cart_session',response.data.message)
    // }

    // useEffect(()=>{
    //   const data = localStorage.getItem('data')
    //   if(data){
    //     const {id} = data
    //     setUserId(id)
    //     handlesession_cart();
    //   }else{
    //     setUserId('')
    //   }
    //   //eslint-disable-next-line
    // 
    
  

  

   
  

 
  
  
 

  

  return (
    <div className='products' key={props.id}>
    <Card key={props.id}   style={{ width: "inherit" }}>
        <Card.Img variant="top" src={props.image}  key = {props.id} id = "prd_image"  />
        <Card.Body>
          <Card.Title>Card Title</Card.Title>
          <Card.Text>
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
            <p>{props.price}</p>
          </Card.Text>
          <div className="product-actions">
            <Button onClick={() => addToCart(navigate('/cart'))}  variant="primary" id='buy_btn'>Buy Now</Button>
            <Button onClick={addToCart} variant="secondary" id='add_btn'>Add to cart</Button>
          
          </div>
        </Card.Body>
      </Card>
      
    </div>
  )
}
