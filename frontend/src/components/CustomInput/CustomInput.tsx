import React from 'react';
import { Input } from 'antd';
import type { InputProps } from 'antd'
import styles from './CustomInput.module.css';

interface CustomInputProps extends InputProps {
    width?: string | number;
}

const CustomInput: React.FC<CustomInputProps> = ({ width = '300px', style, ...rest }) => {
    const mergedStyle = {
        width,
        ...style,
    };

    return (
        <div className={styles.container}>
        <Input style={mergedStyle} {...rest} />
        </div>
    );
};

export default CustomInput;