import React from 'react';
import Container from 'react-bootstrap/Container';
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import { InputArea } from './interaction/InputArea';
import { Transition } from './extras/Transition';
import { OutputArea } from './interaction/OutputArea';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = { input: "", output: "", error: false, loading: false };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(input) {
    // TODO: Post to flask
    this.setState({ output: "" });
  }


  render() {
    return (
      <Container fluid={true} className="App-container">
        <Row className="App-header-row">
          CAS
        </Row>
        <Row className="App-main-row">
          <Col sm={5} className="App-col">
            <InputArea submitHandler={this.handleSubmit}></InputArea>
          </Col>
          <Col className="App-col">
            <Transition loading={this.state.loading}></Transition>
          </Col>
          <Col sm={5} className="App-col">
            <OutputArea output={this.state.output} error={this.state.error}></OutputArea>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App
