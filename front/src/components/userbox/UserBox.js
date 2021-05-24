import React, { Component } from "react";
import "./UserBox.css";
import {urlApi} from "../../configs"
import Button from "react-bootstrap/Button";

export default class UserBox extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null
          }
    }

    handleUploadfile  = (event) => {
        event.preventDefault();
        const formData = new FormData()
        formData.append('file', this.state.selectedFile)
        
        fetch(urlApi + "products/upload", {
             method: 'POST',
             headers: {
                 'Accept': 'application/json',
                 'Content-Type': 'multipart/form-data'
             },
             body: formData
        }).then((response) =>  {
           return response.text();
        })
    }

    onChangeHandler=event=>{
        this.setState({
            selectedFile: event.target.files[0]
          })
    }

    render() {
        return (
            <div>

                Import CSV<br />
                <form onSubmit={this.handleUploadfile} encType="multipart/form-data" ref={el => this.form = el}>                    
                    <input type="file" name="file" onChange={this.onChangeHandler}/>
                    <Button type="submit">Upload</Button>
                </form>
                
                <ul>

                <form onSubmit={this.deleteAll}>                    
                    <Button type="submit">Delete all products</Button>
                </form>
                </ul>

            </div>
        );
    }
}