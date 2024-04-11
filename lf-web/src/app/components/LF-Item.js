import React from "react";
import styles from "../lf_Item.module.css";
//import customData from '../config.json'

export default function LFItem({ data }) {
  const img_path = "/images/" + data.lightFieldAttributes.file;

  return (
    <div className={styles.itemview}>
      <div
        style={{
          flex: 1,
          padding: 10,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div>
          {Object.keys(data.lightFieldAttributes).map((key) => (
            <p>
              {key}: {JSON.stringify(data.lightFieldAttributes[key])}
            </p>
          ))}
        </div>
      </div>
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <img
          src={img_path}
          alt="Description of the image"
          style={{ height: "100%" }}
        />
      </div>
    </div>
  );
}

/*

<div style={{borderStyle: "solid", flex: 1}}>
       <p>type: {data.simulatorAttributes.type}</p>
       <p>position: [{data.simulatorAttributes.position[0]}, {data.simulatorAttributes.position[1]}, {data.simulatorAttributes.position[2]}]</p>
       <p>orientation: [{data.simulatorAttributes.orientation[0]}, {data.simulatorAttributes.orientation[1]}, {data.simulatorAttributes.orientation[2]}]</p>
       </div>

*/
