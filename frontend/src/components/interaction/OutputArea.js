import React from 'react';
import Latex from "react-latex";
import './OutputArea.css';

export class OutputArea extends React.Component {
    render() {
        let output;
        if (this.props.output !== "") {
            output = <Latex>{this.props.output}</Latex>;
        } else if (this.props.error) {
            output = <Latex>Error with no output</Latex>;
        } else {
            output = <Latex>No Output</Latex>;
        }

        return (
            <div className="output-div">
                {output}
            </div>
        );
    }
}
