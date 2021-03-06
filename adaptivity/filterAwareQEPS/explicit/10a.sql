select count(*) from 
cast_info AS ci 
join role_type AS rt on (rt.role = 'actor' AND rt.id = ci.role_id and ci.note LIKE '%(voice)%' AND ci.note LIKE '%(uncredited)%')
join title AS t on (t.production_year > 2005 AND t.id = ci.movie_id)
join char_name AS chn on (chn.id = ci.person_role_id)
JOIN movie_companies AS mc  
on(mc.movie_id = ci.movie_id)
join company_type AS ct on (ct.id = mc.company_type_id)
join company_name AS cn on (cn.country_code = '[ru]' AND cn.id = mc.company_id);