import React, { Component } from "react";
import { Row, Col, Button, } from "react-bootstrap";
import UserBox from '../userbox/UserBox'
import {urlApi} from '../../configs'
import "./Product.css";

export default class Product extends Component {

    constructor(props) {
        super(props);
        this.state = { session: undefined, counter: 0} ;
      }

      componentDidMount() {
        
      }
    
      
    render() {
      return (
            <div className="product-wrapper">
            <div className="product-inner">
                <div className="productContainer">
                    <Row className="fullBox">
                        <Col xs={2} md={2} className="boxcontent">
                            <UserBox users={this.state.users} rooms={this.state.rooms} reload_rooms={this.load_rooms} chats={this.state.chats} session={this.state.session} changeChat={this.changeChat} />
                        </Col>
                        <Col className="boxcontent">
sdfsdfsdfdf
                        </Col>
                    </Row>
                </div>
            </div>
        </div>
        );
    }
}



