import React from "react";
import ReactDOM from "react-dom";
import './Modal.css';

const Modal =props=>{
  
    return (
      props.open? ReactDOM.createPortal(
        <div className = 'modal'>
            <div className = 'content'>
                <div className = 'modal-header'>
                    <h4 className = 'modal-title'>Modal component</h4>
                </div>
                
                <div className = 'modal-body'>
                    Email petition was sent
                </div>
                <div className = 'modal-footer'>
                    <button onClick= {props.close}>Close</button>
                </div>
            </div>
             
        </div>,document.body):null
    );
  }


export default  Modal;
