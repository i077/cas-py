import React from 'react';
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { LiveInput } from "./LiveInput";
import './InputArea.css';

export class InputArea extends React.Component {
    constructor(props) {
        super(props);

        this.state = { input: "", previousSelect: props.selectedText };

        this.textAreaChange = this.textAreaChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    static getDerivedStateFromProps(props, state) {
        if (props.selectedText !== state.previousSelect) {
            return { input: props.selectedText, previousSelect: props.selectedText };
        } else {
            return { input: state.input };
        }
    }

    handleKeyPress(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            this.handleSubmit();
        }
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
                <Form id="input-form" >
                    <Form.Group>
                        <Form.Label>Enter Latex:</Form.Label>
                        <Form.Control as="textarea" rows="6" value={this.state.input} onChange={this.textAreaChange} onKeyUp={this.handleKeyPress} />

                        <LiveInput input={this.state.input} />
                    </Form.Group>
                    <Button onClick={this.handleSubmit}>Submit Latex</Button>
                </Form>
            </div >
        );
    }
}
