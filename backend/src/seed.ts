import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {db} from './db.js';
const filename=fileURLToPath(import.meta.url);const dataPath=path.resolve(path.dirname(filename),'../../dataset/rbi_records.json');
type RecordRow={id:string;name:string;year:number;[key:string]:string|number|null};
const rows=JSON.parse(fs.readFileSync(dataPath,'utf8')) as RecordRow[];
const keys=['gross_open','gross_close','net_open','net_close','advances','tier1','tier2','car','interest_earned','interest_expended','nii','other_income','operating_expenses','net_profit','assets','previous_assets','borrowings','capital','reserves','deposits','lcr'];
async function run(){const c=await db.getConnection();try{await c.beginTransaction();for(const r of rows){await c.execute('INSERT INTO banks(id,name) VALUES (?,?) ON DUPLICATE KEY UPDATE name=VALUES(name)',[r.id,r.name]);const cols=['bank_id','year',...keys];const vals=[r.id,r.year,...keys.map(k=>r[k])];await c.execute(`INSERT INTO financial_records (${cols.join(',')}) VALUES (${cols.map(()=>'?').join(',')}) ON DUPLICATE KEY UPDATE ${keys.map(k=>`${k}=VALUES(${k})`).join(',')}`,vals);}await c.commit();console.log(`Imported ${rows.length} financial records from the supplied RBI workbook`);}catch(e){await c.rollback();throw e}finally{c.release();await db.end();}}
run().catch(e=>{console.error(e);process.exit(1)});
