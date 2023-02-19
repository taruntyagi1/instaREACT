import React from "react";
import axios from "axios";
import { useState,useEffect } from "react";


export const useAuth = () => {
    const [userId, setUserId] = useState("");
  
    useEffect(() => {
      const token_data = JSON.parse(localStorage.getItem("data"));
      if (token_data) {
        setUserId(token_data.id);
      } else {
        setUserId("");
      }
    }, []);
  
    const handleLogin = async (email, password) => {
      const response = await axios.post("http://127.0.0.1:8000/login/", {
        email,
        password,
      });
  
      const data = await response.data;
      const expiresIn = 3600;
  
      localStorage.setItem("expire", expiresIn);
      localStorage.setItem("data", JSON.stringify(data));
  
      setUserId(data.id);
  
      setTimeout(() => {
        localStorage.removeItem("data");
        localStorage.removeItem("expire");
        setUserId("");
      }, expiresIn * 1000);
    };
  
    
  
    const handleSessionCart = async (cart) => {
      const response = await axios.post(
        "http://127.0.0.1:8000/session_cart/",
        {
          cart,
          userId,
        }
      );
      console.log(response.data.message);
    };
  
    return {
      userId,
      handleLogin,
    //   handleLogout,
      handleSessionCart,
    };
  };