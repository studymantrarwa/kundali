const SM=supabase.createClient(STUDY_MANTRA_CONFIG.SUPABASE_URL,STUDY_MANTRA_CONFIG.SUPABASE_ANON_KEY);
async function me(){const {data:{user}}=await SM.auth.getUser();if(!user){location.href='/auth.html';return null}const {data}=await SM.from('profiles').select('*').eq('id',user.id).single();return data}
async function logout(){await SM.auth.signOut();location.href='/auth.html'}
function esc(x){return String(x??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}