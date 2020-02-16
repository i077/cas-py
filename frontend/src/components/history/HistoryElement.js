import React from 'react';
import TeX from '@matejmazur/react-katex';
import './HistoryElement.css';

export class HistoryElement extends React.Component {
    constructor(props) {
        super(props);

        this.elementClick = this.elementClick.bind(this);
    }

    elementClick() {
        this.props.handleClick(this.props.historyItem);
    }

    render() {
        return (
            <div className="history-item-div" onClick={this.elementClick}>
                <TeX
                    math={this.props.historyItem}
                    errorColor={'#cc0000'}
                    settings={{ macros: { '\\dd': '\\mathrm{d}' } }}
                />
            </div>
        );
    }
}
