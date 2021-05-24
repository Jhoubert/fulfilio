import React, { Component } from "react";
import Button from "react-bootstrap/Button";
import "./ChatBox.css";

export default class ChatBox extends Component {
    
    constructor(props) {
        super(props);
        this.state = { counter: 0, messages: [], msg: ""} ;
        this.sendMsg = this.sendMsg.bind(this);
        this.myFormRef = React.createRef();
        this.handleChange = this.handleChange.bind(this);
        this.handleKU = this.handleKU.bind(this);
    }

    sendMsg(event){
        event.preventDefault();
        let msg_payload = {
            to: this.props.to.user,
            message: event.target.msgTxt.value,
            room_id: this.props.to.room_id
        }
        this.setState({msg: ""});
        this.props.send(msg_payload);
    }

    handleKU(event) {
        event.preventDefault();
        if(event.keyCode === 13 && event.shiftKey === false) {
            var ev = new Event('submit', {
                'bubbles'    : true,
                'cancelable' : true
            });
            this.myFormRef.dispatchEvent(ev);
        }
      }

    handleChange(event){
        this.setState({msg: event.target.msg});
    }

    componentDidMount() {
        if (this.props.messages.length>0){
            this.executeScroll();
        }
    }
    

    render() {

        setTimeout(() => {if (this.props.messages.length > 0){
            this.executeScroll();
        }},100);


        const result = this.props.messages.map((message, k) => 
            <div key={k} className={ message.from === this.props.session.user ? "received" : "sended"} ref={(ref) => this.myRef=ref}>
                <p>{ message.from === this.props.session.user ? '' : <small style={{color:'gray'}}>{message.from}:</small>} {message.message}</p>
                &nbsp;<span className="time">{message.date}</span>
            </div>
        );


        return (
            <div className="ct">
                <b>{this.props.to.user}</b> 
                
            <div id="chatContainer">

                {result}

            </div>
                
            <div id="bottomPanel">
                <div>
                    <form onSubmit={this.sendMsg} ref={el => this.myFormRef = el}>
                    <table className="tb">
                        <tr>
                            <td width={"90%"}><textarea name="msgTxt" value={this.state.msg} onChange={this.handleChange} onKeyUp={this.handleKU} ></textarea></td>
                            <td><Button type="submit" className="sendbtn"> Send </Button></td>
                        </tr>
                    </table>
                    </form>
                   
                </div>
            </div>

                    
                
            </div>
        );
        
    }

    executeScroll = () => {this.myRef && this.myRef.scrollIntoView()}
}