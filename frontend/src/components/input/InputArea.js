import React from 'react';
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { LiveInput } from "./LiveInput";
import './InputArea.css';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

export class InputArea extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            input: "",
            replacedInput: "",
            previousSelect: props.selectedText
        };

        this.textAreaChange = this.textAreaChange.bind(this);

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleReset = this.handleReset.bind(this);
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

    getReplacedInput(input) {
        var re = /[$]\d+/g, replace = re.exec(input);

        while (replace !== null) {
            const replNum = parseInt(replace[0].substr(1, replace[0].length - 1));
            const foundCalc = this.props.history.find((calc) => calc.id === replNum);

            if (foundCalc === undefined) {
                input = input.replace(replace[0], '\\left( \\text{Reference Not Found} \\right)');
            } else if (foundCalc.output === "") {
                input = input.replace(replace[0], '\\left( \\text{Reference has No Output} \\right)');
            } else {
                input = input.replace(replace[0], '\\left(' + foundCalc.output + '\\right)');
            }

            replace = re.exec(input);
        }
        return input;
    }

    textAreaChange(e) {
        const val = e.target.value;
        this.setState({
            input: val,
            replacedInput: this.getReplacedInput(val)
        });
    }

    handleSubmit() {
        this.props.submitHandler(this.state.replacedInput);
    }

    handleReset() {
        this.props.resetHandler();
    }

    render() {
        return (
            <div className="input-div">
                <Form id="input-form" >
                    <Form.Group>
                        <Row>
                            <Col>
                                <Form.Control as="textarea" rows="6" value={this.state.input} onChange={this.textAreaChange} onKeyUp={this.handleKeyPress} />
                            </Col>
                            <Col>
                                <LiveInput input={this.state.replacedInput} />
                            </Col>
                        </Row>
                        <Row className='input-button-row'>
                            <Button onClick={this.handleSubmit}>Submit LaTeX</Button>
                            <Button onClick={this.handleReset}>Reset State</Button>
                        </Row>
                    </Form.Group>
                </Form>
            </div >
        );
    }
}
