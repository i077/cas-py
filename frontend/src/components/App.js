import React from 'react';
import Container from 'react-bootstrap/Container';
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import { InputArea } from './input/InputArea';
import { OutputArea } from './output/OutputArea';
import { Transition } from './extras/Transition';
import { History } from './input/History';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = { input: "", output: "", history: [], error: false, loading: false };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(input) {
    this.setState({ loading: true });

    fetch('http://localhost:5000/run', {
      method: 'POST',
      body: JSON.stringify({ input: input })
    })
      .then(response => response.json())
      .then(response => {
        const new_history = this.state.history.concat(input);
        this.setState({
          output: response.output,
          error: response.error,
          history: new_history,
          loading: false
        });
      });
  }

  render() {
    return (
      <Container fluid={true} className="App-container">
        <Row className="App-header-row">
          CAS
        </Row>
        <Row className="App-main-row">
          <Col sm={5} className="App-col">
            <History history_list={this.state.history} />
            <InputArea submitHandler={this.handleSubmit} />
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