import React from 'react';
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { LiveInput } from "./LiveInput";
import './InputArea.css';

export class InputArea extends React.Component {
    constructor(props) {
        super(props);

        this.state = { input: "" };

        this.textAreaChange = this.textAreaChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    textAreaChange(e) {
        this.setState({ input: e.target.value });
    }

    handleSubmit() {
        this.props.submitHandler(this.state.input);
    }


    render() {
        return (
            <div className="input-div">
                <Form>
                    <Form.Group controlId="exampleForm.ControlTextarea1">
                        <Form.Label>Enter Latex:</Form.Label>
                        <Form.Control as="textarea" rows="10" onChange={this.textAreaChange} />
                        <LiveInput input={this.state.input} />
                    </Form.Group>
                    <Button onClick={this.handleSubmit}>Submit Latex</Button>
                </Form>
            </div>
        );
    }
}
