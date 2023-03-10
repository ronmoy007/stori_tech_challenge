import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logo from './Stori-horizontal-11.jpg'
import Modal from './Modal';

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState([])
  const [months, setMonths] = useState([])
  const [showModal, setShowModal] = useState(false);

  try {
    useEffect(() => {
      (async () => {
        const response = await axios.get(`${process.env.REACT_APP_URL_BACKEND}/get-data`);
        setSummary(response.data.summary_data);
        setMonths(response.data.months_data);        
      })();
    }, []);
  } catch (error) {
    console.error(error);
  }

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  }
 
  const handleSubmit = async () => {
    const data_file = new FormData();
    data_file.append('file', file);

    try {
      var response = await axios.post(`${process.env.REACT_APP_URL_BACKEND}/process-file`, data_file);

      response = await axios.get(`${process.env.REACT_APP_URL_BACKEND}/get-data`);
      setSummary(response.data.summary_data);
      setMonths(response.data.months_data);
      
    } catch (error) {
      console.error(error);
    }
  }
 
  const handleSendMail = async (client_id) => {
    var payload = {client_id}
    axios.post(`${process.env.REACT_APP_URL_BACKEND}/send-mail`, payload);
    setShowModal(true);
  }

  function isButtonEnabled(reference_value) {
    return !(reference_value === null);
  }

  function handleClose() {
    setShowModal(false);
  }

  return (
    <div>
      <style>{
      `table, th, td{
        border:1px 
        solid black;
      }`
      }
      </style>
      <img style={{ width: "50%", height: "50%" }} src={logo} alt="Stori logo" />
      <br></br><br></br>
      <input type="file" onChange={handleFileChange} />
      <button disabled={!isButtonEnabled(file)} onClick={handleSubmit} >Upload</button>
      <Modal open = {showModal} close = {handleClose}/>
      <br></br><br></br>
      <table style={{width:'100%'}}>
        <caption><strong>Summary of transactions</strong></caption>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Email</th>
            <th>Total balance</th>
            <th>Credit average</th>
            <th>Debit average</th>
            <th>Send mail</th>
          </tr>
        </thead>
        <tbody>
          {summary.map(item_summary => (
            <tr key={item_summary[0]}>
              <td align='left'>{item_summary[0]}</td>
              <td align='left'>{item_summary[1]}</td>
              <td align='left'>{item_summary[2]}</td>
              <td align='right'>{item_summary[5]}</td>
              <td align='right'>{item_summary[3]}</td>
              <td align='right'>{item_summary[4]}</td>
              <td align='center'>
                <button onClick={() => handleSendMail(item_summary[0])} disabled={!isButtonEnabled(item_summary[3])} >Send email to {item_summary[1]}</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <br></br><br></br>
      <table style={{width:'100%'}}>
      <caption><strong>Summary of transactions by month</strong></caption>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Year</th>
            <th>Month name</th>
            <th>No. of transactions by month</th>
            <th>Total balance by month</th>
            <th>Total credit by month</th>
            <th>Average credit by month</th>
            <th>Total debit by month</th>
            <th>Average debit by month</th>
          </tr>
        </thead>
        <tbody>
          {months.map(item_months => (
            <tr key={item_months[0]+"_"+item_months[2]+"_"+item_months[3]}>
              <td align='left'>{item_months[0]}</td>
              <td align='left'>{item_months[1]}</td>
              <td align='left'>{item_months[2]}</td>
              <td align='left'>{item_months[4]}</td>
              <td align='right'>{item_months[5]}</td>
              <td align='right'>{item_months[6]}</td>
              <td align='right'>{item_months[7]}</td>
              <td align='right'>{item_months[8]}</td>
              <td align='right'>{item_months[9]}</td>
              <td align='right'>{item_months[10]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
