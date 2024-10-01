import * as React from 'react';

import { Button } from '@alifd/next';
import './index.scss';
import { createElement } from 'react';

export interface NewMaterialProps {
  title?: string;
  description?: string;
  backgroundImage?: string;
}

const NewMaterial: React.FC<NewMaterialProps> = function NewMaterial({
  title,
  description,
  backgroundImage,
}){
  return(
    <>
      <div className="new-material" style={{background:'url(${backgroundImage})'}}>
        {title}
      </div>
      <div>
        {description}
      </div>
      <div>
        <Button type="normal">详情</Button>
      </div>
    </>
  );

};


NewMaterial.defaultProps = {
  title: 'Title',
  description: 'This is a description',
  backgroundImage: ''
}

export default NewMaterial;
