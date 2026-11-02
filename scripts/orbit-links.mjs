// One Orbit zip, many doors.
// public/os/Orbit.zip is the only real file. Every release overwrites it.
// Older download addresses (in emails already sent) are copied from it at
// build time, so every button anyone ever got hands out the newest Orbit.
// To keep another old address alive, add its file name here.
import { copyFileSync } from "node:fs";

const OLD_ADDRESSES = ["Orbit-v0.4.zip", "Orbit-v0.3.3.zip"];
for (const name of OLD_ADDRESSES) {
  copyFileSync("public/os/Orbit.zip", `public/os/${name}`);
  console.log(`orbit-links: os/${name} = os/Orbit.zip`);
}
