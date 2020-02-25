import React from 'react';
import TeX from '@matejmazur/react-katex';
import './LiveInput.css';

export class LiveInput extends React.Component {
    render() {
        return (
            <div className="live-input-div">
                <TeX
                    math={this.props.input}
                    errorColor={'#cc0000'}
                    settings={{ macros: { '\\dd': '\\mathrm{d}' } }}
                />
            </div>
        );
    }
}
