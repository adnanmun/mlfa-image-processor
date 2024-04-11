import Image from "next/image";
import LFItem from "./components/LF-Item";
import styles from "./page.module.css";
import customData from "./config.json";

export default function Home() {
  //const customData = require('./config.json')
  //console.log(customData)

  const LF_list = customData.map((item) => {
    return <LFItem data={item}></LFItem>;
  });

  return (
    <main className={styles.main}>
      <div className={styles.list}>
        <div className={styles.attributes}>
          <h2>LightField</h2>
          <h2>Image</h2>
        </div>
        {LF_list}
      </div>
    </main>
  );
}
