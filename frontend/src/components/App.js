import React from 'react';

import Container from 'react-bootstrap/Container';
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Button from 'react-bootstrap/Button';

import { InputArea } from './input/InputArea';
import { History } from './history/History';

import Session from "./session/session";
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = { history: [], selectedText: "" };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleReset = this.handleReset.bind(this);
    this.handleHistoryClick = this.handleHistoryClick.bind(this);
  }

  componentDidMount() {
    if (Session.getSession() === undefined) {
      this.createNewSession();
    } else {
      this.getHistory();
    }
  }

  createNewSession() {
    fetch('http://localhost:5000/create-session', {
      method: 'POST',
      body: JSON.stringify({ id: Session.getSession() })
    })
      .then(response => response.json())
      .then(response => {
        Session.setSession(response.id);
      });
  }

  handleReset() {
    if (Session.getSession() !== undefined) {
      this.setState({
        history: [],
        selectedText: "",
      });
      this.createNewSession();
    }
  }

  handleSubmit(input) {
    fetch('http://localhost:5000/run', {
      method: 'POST',
      body: JSON.stringify({ id: Session.getSession(), input: input })
    })
      .then(response => response.json())
      .then(response => {
        const history = this.state.history;
        const nextId = (history.length === 0) ? 1 : history[history.length - 1].id + 1;

        const new_history = this.state.history.concat({
          id: nextId,
          input: input,
          error: response.error,
          output: response.output
        });

        this.setState({
          history: new_history,
        });

        this.updateHistory();
      });
  }

  updateHistory() {
    fetch('http://localhost:5000/update-history', {
      method: 'POST',
      body: JSON.stringify({
        id: Session.getSession(),
        calculation: this.getLastCalculation()
      })
    });
  }

  getHistory() {
    fetch('http://localhost:5000/get-history', {
      method: 'POST',
      body: JSON.stringify({ id: Session.getSession() })
    })
      .then(response => response.json())
      .then(response => {
        this.setState({
          history: response.history,
        });
      });
  }

  handleHistoryClick(calculation) {
    this.setState({
      selectedText: calculation.input,
    });
    this.forceUpdate();
  }

  render() {
    return (
      <Container fluid={true} className="App-container">
        <Row className="App-header-row">
          CAS
        </Row>
        <Row className="App-main-row">
          <Col className="App-col">
            <History history={this.state.history} handleHistory={this.handleHistoryClick} />
            <InputArea submitHandler={this.handleSubmit} history={this.state.history} selectedText={this.state.selectedText} />
          </Col>
        </Row>
        <Row className="App-footer-row">
          <Button onClick={this.handleReset}>Reset Session</Button>
        </Row>
      </Container>
    );
  }
}

export default App
