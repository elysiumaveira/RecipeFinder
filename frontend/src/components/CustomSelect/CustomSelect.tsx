import React from 'react';
import { Select } from 'antd';
import type { SelectProps } from 'antd'
import styles from './CustomSelect.module.css';

interface CustomSelectProps extends SelectProps {
    width?: string | number;
}

const CustomSelect: React.FC<CustomSelectProps> = ({ width = '300px', style, ...rest }) => {
    const mergedStyle = {
        width,
        ...style,
    };

    return (
        <div className={styles.container}>
        <Select style={mergedStyle} {...rest} />
        </div>
    );
};

export default CustomSelect;