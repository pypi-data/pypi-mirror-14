/*******************************************************************************
 * Copyright 2013-2016 Aerospike, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

#include <Python.h>
#include <aerospike/as_error.h>
#include <aerospike/as_policy.h>

#define MAX_CONSTANT_STR_SIZE 512

/*
 *******************************************************************************************************
 *Structure to map constant number to constant name string for Aerospike constants.
 *******************************************************************************************************
 */

enum Aerospike_serializer_values {
	SERIALIZER_NONE,
	SERIALIZER_PYTHON, /* default handler for serializer type */
	SERIALIZER_JSON,
	SERIALIZER_USER,
};

typedef struct Aerospike_Constants {
    long    constantno;
    char    constant_str[MAX_CONSTANT_STR_SIZE];
}AerospikeConstants;

typedef struct Aerospike_JobConstants {
    char job_str[MAX_CONSTANT_STR_SIZE];
    char exposed_job_str[MAX_CONSTANT_STR_SIZE];
}AerospikeJobConstants;
#define AEROSPIKE_CONSTANTS_ARR_SIZE (sizeof(aerospike_constants)/sizeof(AerospikeConstants))
#define AEROSPIKE_JOB_CONSTANTS_ARR_SIZE (sizeof(aerospike_job_constants)/sizeof(AerospikeJobConstants))

as_status pyobject_to_policy_admin(as_error * err, PyObject * py_policy,
									as_policy_admin * policy,
									as_policy_admin ** policy_p,
									as_policy_admin * config_admin_policy);

as_status pyobject_to_policy_apply(as_error * err, PyObject * py_policy,
									as_policy_apply * policy,
									as_policy_apply ** policy_p,
									as_policy_apply * config_apply_policy);

as_status pyobject_to_policy_info(as_error * err, PyObject * py_policy,
									as_policy_info * policy,
									as_policy_info ** policy_p,
									as_policy_info * config_info_policy);

as_status pyobject_to_policy_query(as_error * err, PyObject * py_policy,
									as_policy_query * policy,
									as_policy_query ** policy_p,
									as_policy_query * config_query_policy);

as_status pyobject_to_policy_read(as_error * err, PyObject * py_policy,
									as_policy_read * policy,
									as_policy_read ** policy_p,
									as_policy_read * config_read_policy);

as_status pyobject_to_policy_remove(as_error * err, PyObject * py_policy,
									as_policy_remove * policy,
									as_policy_remove ** policy_p,
									as_policy_remove * config_remove_policy);

as_status pyobject_to_policy_scan(as_error * err, PyObject * py_policy,
									as_policy_scan * policy,
									as_policy_scan ** policy_p,
									as_policy_scan * config_scan_policy);

as_status pyobject_to_policy_write(as_error * err, PyObject * py_policy,
									as_policy_write * policy,
									as_policy_write ** policy_p,
									as_policy_write * config_write_policy);

as_status pyobject_to_policy_operate(as_error * err, PyObject * py_policy,
                                    as_policy_operate * policy,
                                    as_policy_operate ** policy_p,
									as_policy_operate * config_operate_policy);

as_status pyobject_to_policy_batch(as_error * err, PyObject * py_policy,
                                   as_policy_batch * policy,
                                   as_policy_batch ** policy_p,
								   as_policy_batch * config_batch_policy);

as_status declare_policy_constants(PyObject *aerospike);

void set_scan_options(as_error *err, as_scan* scan_p, PyObject * py_options);
