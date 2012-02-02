#!/usr/bin/python

import MySQLdb as mdb
import sys

con = mdb.connect('192.168.1.199', 'risk', 'risk1234$', 'riskAssessment')
data = []

table = raw_input('Enter the table to collect data from:  ')
model = raw_input('Enter the model:  ')

# file to output
f = open('/var/www/vhosts/azyas/app/DataFixtures/ORM/Phase2/'+model+'.php', 'w')

f.write('<?php\n')
f.write('namespace Application\\DataFixtures\\ORM;\n')
f.write("\n")
f.write("use Doctrine\\Common\\DataFixtures\\AbstractFixture;\n")
f.write("use Doctrine\\Common\\DataFixtures\\OrderedFixtureInterface;\n")
f.write("use Risk\\CasePlanBundle\\Entity\\" + model + ";\n\n\n")

f.write("class load" + model + " extends AbstractFixture implements OrderedFixtureInterface\n")
f.write("{\n")
f.write("    public function load($manager)\n")
f.write("    {\n")
f.write("\n")

with con:

    cur = con.cursor()
    cur.execute("SELECT * FROM " + table +"" )

    rows = cur.fetchall()

    desc = cur.description

    for d in desc:
        print d[0]
        data.append(raw_input('Enter method for ' + d[0] + ':  '))

    counter = 0
    for row in rows:

        counter += 1
        variable_name = model + str(counter)
        f.write('       $' + variable_name + ' = new ' + model + '();\n')

        for i in range(len(desc)):

            if(data[i] != ''):
                value = row[i]

                if(desc[i][0] == 'assessment_type_id'):
                    value += 6

                if(desc[i][0] == 'question_id'):
                    value += 72

                f.write("       $" + variable_name + "->" + data[i] + "('" + str(value) + "');\n")

        f.write("       $manager->persist('" + variable_name +"',$" + variable_name +");\n")
        f.write("\n")


f.write("\n        $mananger->flush();\n")
f.write("    }\n\n")
f.write("    public function getOrder()\n")
f.write("    {\n")
f.write("        return 1;\n")
f.write("    }\n\n")
f.write("}")
f.close()
