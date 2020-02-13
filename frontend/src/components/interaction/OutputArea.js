import React from 'react';
import TeX from '@matejmazur/react-katex';
import './OutputArea.css';

export class OutputArea extends React.Component {
    render() {
        let output;
        if (this.props.output !== "") {
            output = <TeX
                math={this.props.output}
                errorColor={'#cc0000'}
                settings={{ macros: { '\\dd': '\\mathrm{d}' } }}
            />;
        } else if (this.props.error) {
            output = <p>Error with no output</p>;
        } else {
            output = <p>No Output</p>;
        }

        return (
            <div className="output-area-div">
                {output}
            </div>
        );
    }
}
