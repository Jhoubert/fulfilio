import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {urlApi} from '../../configs'
import "./Login.css";
import { useHistory } from "react-router-dom";
import Cookies from 'universal-cookie';


export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const history = useHistory();
  
  function validateForm() {
    return username.length > 0 && password.length > 0;
  }

  function handleSubmit(event) {

    var body = {"user": event.target.username.value, "password": event.target.password.value};

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include', mode: 'cors',
    };


    fetch(urlApi + "auth/login", requestOptions)
    .then(response => response.json())
    .then(function (data){
        if ('jwt' in data){
          const cookies = new Cookies();
          cookies.set('auth', data.jwt, { path: '/' });
          history.push("/products");
        }else{
          setMsg(data.msg)
        }
      }.bind(this)
    );

    event.preventDefault();
  }

  return (
    <div className="auth-wrapper">
        <div className="auth-inner">
            <div className="Login">
                <Form onSubmit={handleSubmit}>
                    <Form.Group size="lg" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        autoFocus
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    </Form.Group>
                    <Form.Group size="lg" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    </Form.Group>
                    <Button block size="lg" type="submit" disabled={!validateForm()}>
                    Login
                    </Button>
                    <Form.Label>{msg}</Form.Label>
                </Form>
            </div>
        </div>
    </div>
  );
}